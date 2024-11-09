import asyncio
import time
from typing import List, Tuple

from box import Box
from loguru import logger

from .const import TaskExecType, ExecStatus, DB_REF_KEY_SUFFIX, KAFKA_KEY_SUFFIX
from .db_register import get_db
from .executions import TaskExecutionInfo, TaskNodeExecutionInfo
from .kafka_register import get_kafka
from .task import TaskInfo, TaskNodeGraph, TaskNodeInfo

__all__ = ['TASK_REGISTRY_CENTER', 'TASK_NODE_REGISTRY_CENTER', 'PissyTaskExecutionException', 'task', 'task_node',
           'TaskNodeRegistry', 'TaskRegistry']

type NodeId = str
type TaskExecutionType = str


class TaskRegistry(object):
    """
    注册信息
    """
    func: any
    module_name: str

    def __str__(self):
        return f"{self.module_name}.{self.func.__name__}"


class TaskNodeRegistry(object):
    """
    注册信息
    """
    func: any
    module_name: str
    dep_on: List[str] = []

    def __str__(self):
        return f"{self.module_name}.{self.func.__name__}"


TASK_REGISTRY_CENTER: dict[TaskExecutionType, TaskRegistry] = {}  # 任务注册中心
TASK_NODE_REGISTRY_CENTER: dict[NodeId, TaskNodeRegistry] = {}  # 节点注册中心


class PissyTaskExecutionException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


def task(task_execution_type: TaskExecutionType, module_name=None):
    """
    自动注册task,module不存在,直接手工import
    @param task_execution_type:
    @param module_name:
    @return:
    """

    def wrapper(func):
        tr: TaskRegistry = TaskRegistry()
        tr.module_name = module_name
        tr.func = func
        TASK_REGISTRY_CENTER[task_execution_type] = tr
        logger.info(f'registry task={tr} success')
        return func

    return wrapper


def task_node(node_id: NodeId, module_name=None, dep_on: List[str] = None):
    """
    自动注册node,module不存在,直接手工import
    @param dep_on: 前置节点列表,多个的话逗号分割
    @param node_id:节点任务编号
    @param module_name:
    @return:
    """
    import inspect
    def is_async_function(func):
        return inspect.iscoroutinefunction(func)

    def wrapper(func):
        if not is_async_function(func):
            logger.error(f'{func} add the task_node annotation, but it is not async function,can not be registered')
        tnr: TaskNodeRegistry = TaskNodeRegistry()
        tnr.module_name = module_name
        tnr.func = func
        if dep_on is not None:
            dos: List[str] = dep_on
            tnr.dep_on = dos
        TASK_NODE_REGISTRY_CENTER[node_id] = tnr
        logger.info(f'register task node={tnr} success')
        return func

    return wrapper


def __assemble_task_node_ref_params_dict(node_id: str, task_config_box: Box) -> dict[str, any]:
    """
    填充节点引用参数
    @param task_config_box:
    @param node_id
    @return:
    """
    if not task_config_box.__contains__(node_id):
        return {}
    node_config_box: Box = task_config_box.get(node_id)
    node_param_dict: dict[str, any] = node_config_box.to_dict()
    # 对于_db结尾的参数特殊处理,后面看看有没有更优雅的方法
    node_db_refs: List[str] = list(filter(lambda x: x.endswith(DB_REF_KEY_SUFFIX), node_config_box.keys(), ))
    for db_ref in node_db_refs:
        node_param_dict[db_ref] = get_db(db_sign=node_config_box.get(db_ref))
    # kafka 引用变量处理
    kafka_refs: List[str] = list(filter(lambda x: x.endswith(KAFKA_KEY_SUFFIX), node_config_box.keys(), ))
    for kafka_ref in kafka_refs:
        node_param_dict[kafka_ref] = get_kafka(kafka_sign=node_config_box.get(kafka_ref))
    return node_param_dict


def __to_async_node_func(node_tuple: Tuple[NodeId, TaskNodeRegistry],
                         node_cxt: dict[NodeId, any] | None, task_execution_info: TaskExecutionInfo, ) -> (
        Tuple)[any, TaskNodeExecutionInfo]:
    """
    transfer node func to async task
    :param node_tuple:
    :param node_cxt:
    :param task_execution_info:
    :return:
    """
    node_id, tnr = node_tuple
    if node_cxt is None:
        node_cxt = {}

    node_func = tnr.func
    task_node_execution: TaskNodeExecutionInfo = TaskNodeExecutionInfo()
    task_node_execution.node_id = node_id
    task_node_execution.task_execution_info = task_execution_info
    task_node_execution.node_result_dict = node_cxt
    task_node_execution.curr_task_node_status = ExecStatus.DING
    task_node_execution.start_time = time.time()
    # 填充节点运行参数
    task_config_box: Box = task_execution_info.task_info.task_config
    task_node_execution.node_param_dict = __assemble_task_node_ref_params_dict(node_id=node_id,
                                                                               task_config_box=task_config_box)
    if task_config_box.__contains__(node_id):
        node_config_box: Box = task_config_box.get(node_id)

        node_param_dict: dict[str, any] = node_config_box.to_dict()
        node_db_refs: List[str] = list(filter(lambda x: x.endswith('_db'), node_config_box.keys(), ))
        for db_ref in node_db_refs:
            node_param_dict[db_ref] = get_db(db_sign=node_config_box.get(db_ref))
        task_node_execution.node_param_dict = node_param_dict

    node1 = asyncio.create_task(node_func(task_node_execution))
    return node1, task_node_execution


async def recursive_node_execution(curr_depth: int, task_execution_info: TaskExecutionInfo | None,
                                   task_node_g: TaskNodeGraph, may_used_node_res: dict[NodeId, any]) -> None:
    """
    递归异步执行函数，按深度来执行
    @param curr_depth:
    @param task_execution_info:
    @param task_node_g:
    @param may_used_node_res:
    @return:
    """
    # 当前深度下没有绑定节点,任务执行结束
    curr_level_nodes: List[TaskNodeInfo] = task_node_g.task_node_tree.get(curr_depth, [])
    if curr_level_nodes is None or len(curr_level_nodes) == 0:
        return
    all_child_nodes: List[Tuple[NodeId, any]] = []
    # 当前每个节点执行转换成coroutine
    curr_level_tasks_list = []
    for i in curr_level_nodes:
        tmp_node_id: NodeId = i.node_id
        # 获取注册节点信息
        tmp_node_registry: TaskNodeRegistry = TASK_NODE_REGISTRY_CENTER.get(tmp_node_id, None)
        if tmp_node_registry is None:
            raise PissyTaskExecutionException(f'can not find the node_id={tmp_node_id} in the register.')
        # 获取当前执行节点关联的上下文塞到当前节点执行上下文中,通过获取当前节点所有父节点列表
        tmp_parent_nodes: List[TaskNodeInfo] = task_node_g.get_parent_nodes(tmp_node_id)
        tmp_node_cxt: dict[NodeId, any] = {}
        for j in tmp_parent_nodes:
            tmp_node_cxt[j.node_id] = may_used_node_res.get(j.node_id, None)
        logger.info(f'ready to execute node= {i.node_id} in depth={curr_depth}')
        tmp_bind_coro, tmp_node_execution = __to_async_node_func((i.node_id, tmp_node_registry), node_cxt=tmp_node_cxt,
                                                                 task_execution_info=task_execution_info)
        curr_level_tasks_list.append((tmp_node_id, tmp_bind_coro, tmp_node_execution))
    # 采集各个coro的结果
    coro_res: dict[NodeId, any] = {}
    for k in curr_level_tasks_list:
        k_node_id, k_coro, k_node_execution = k
        coro_res[k_node_id] = await k_coro
        k_node_execution.curr_task_node_status = ExecStatus.DONE
        k_node_execution.stop_time = time.time()
        logger.info(
            f'node={k_node_id} executed done, it spends {(k_node_execution.stop_time - k_node_execution.start_time):.2f} seconds.')
    # 假设a节点的子节点跨深度了,需要继续往下传
    for key in may_used_node_res.keys():
        res = may_used_node_res.get(key)
        # 通过判断上个结果节点的每个字节点都跨深度判断是否要继续往下传递
        sub_nodes: List[TaskNodeInfo] = task_node_g.get_child_nodes(key)
        if sub_nodes is None or len(sub_nodes) == 0:
            continue
        next_depth_nodes: List[TaskNodeInfo] = task_node_g.task_node_tree.get(curr_depth + 1, [])
        if next_depth_nodes is None or len(next_depth_nodes) == 0:
            continue
        if not all(item in next_depth_nodes for item in sub_nodes):
            coro_res[key] = res
    curr_depth = curr_depth + 1
    await recursive_node_execution(curr_depth=curr_depth, task_execution_info=task_execution_info,
                                   task_node_g=task_node_g,
                                   may_used_node_res=coro_res)


# 非集群模式下的任务执行
@task(task_execution_type=TaskExecType.LOCAL.name)
async def run_task_in_local(task_execution_info: TaskExecutionInfo):
    """
     A----->B---------->F
     |                  |
      ----->C---->D------
            |           |
            ----->E------
    :param task_execution_info:
    :return:
    """
    logger.info("execute task info local mod")
    # 任务执行
    task_info: TaskInfo = task_execution_info.task_info
    if task_info is None:
        logger.error("can't find binding task, quit.")
        return
    logger.info("start to get startup nodes for task = {}.", task_info.task_exec_type)
    task_node_g: TaskNodeGraph = task_info.node_graph
    startup_nodes: List[TaskNodeInfo] = task_node_g.get_startup_nodes()
    if startup_nodes is None or len(startup_nodes) == 0:
        raise PissyTaskExecutionException(f"can't find any startup nodes for task={task_info.task_id}")

    # 初始化注册函数
    await recursive_node_execution(curr_depth=0, task_execution_info=task_execution_info, task_node_g=task_node_g,
                                   may_used_node_res={})
    # task_execution_info.curr_task_status = ExecStatus.DING
    task_execution_info.stop_time = time.time()
    logger.info(
        f'execute task done. it spends {(task_execution_info.stop_time - task_execution_info.start_time):.2f} seconds. ', )
