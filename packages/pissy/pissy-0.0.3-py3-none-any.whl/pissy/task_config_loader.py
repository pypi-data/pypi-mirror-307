import json
from typing import List

from box import Box
from loguru import logger

from .const import TaskExecType
from .db_register import register_db
from .executions import TaskSched
from .kafka_register import register_kafka
from .sched import ExecutionAlwaysSched, ExecutionOnceSched
from .task import TaskInfo, TaskNodeInfo


def __try_to_init_db(task_config_box: Box):
    """
    初始化db
    @param task_config_box:
    @return:
    """
    if not task_config_box.__contains__('datasource'):
        return
    datasource_box: Box = task_config_box.datasource
    for db_ref in datasource_box.keys():
        db_config_box: Box = datasource_box.get(db_ref)
        register_db(db_sign=db_ref, db_config=db_config_box.to_dict())
        logger.info(f'register db_ref= {db_ref} datasource success.')


def __try_to_init_kafka(task_config_box: Box):
    """
    初始化kafka
    @param task_config_box:
    @return:
    """
    if not task_config_box.__contains__('kafka'):
        return
    kafka_box: Box = task_config_box.kafka
    for kafka_ref in kafka_box.keys():
        kafka_config_box: Box = kafka_box.get(kafka_ref)
        register_kafka(kafka_sign=kafka_ref, kafka_config=kafka_config_box.to_dict())
        logger.info(f'register kafka_ref={kafka_ref} kafka success.')


def create_task_from_json(task_config_json: str) -> TaskInfo:
    """
    task config json可参考task_demo.json
    @param task_config_json:
    @return:
    """
    logger.info(f'start to parse task config json:{task_config_json}')
    task_info = TaskInfo()
    # 首先检查必须是json格式
    # 检查数据
    # 数据解析
    task_config_dict: dict[str, any] = json.loads(task_config_json)
    # 转成box对象
    task_config_box: Box = Box(task_config_dict)
    task_info.task_name = task_config_box.task_name
    task_info.task_exec_type = TaskExecType.LOCAL.name
    task_info.task_config = task_config_box
    default_task_sched: TaskSched = ExecutionOnceSched()
    task_info.sched_info = default_task_sched
    # 处理节点映射
    nodes_rel_str: str = task_config_box.nodes
    # ['a->b,c', 'a->d']
    nodes_rel_lst: List[str] = nodes_rel_str.split(';')
    for rel_str in nodes_rel_lst:
        parent_node_id: str = rel_str.split('->')[0]
        sub_node_lst: List[str] = rel_str.split('->')[1].split(',')
        parent_child_node_list: List[tuple[str, str]] = list(zip([parent_node_id for _ in range(len(sub_node_lst))],
                                                                 sub_node_lst))
        for it in parent_child_node_list:
            p_node_id: str = it[0]
            p_node: TaskNodeInfo = TaskNodeInfo()
            p_node.node_id = p_node_id
            c_node_id: str = it[1]
            if c_node_id is None or len(c_node_id) == 0:
                task_info.node_graph.add_node_pair(p_node, None)
            else:
                c_node: TaskNodeInfo = TaskNodeInfo()
                c_node.node_id = c_node_id
                task_info.node_graph.add_node_pair(p_node, c_node)
    # 解析每个节点深度
    task_info.node_graph.build_node_tree()
    logger.info('init task info done.')
    # 初始化数据源并注册
    __try_to_init_db(task_config_box)
    # 初始化kafka
    __try_to_init_kafka(task_config_box)
    # 包含drn,默认使用while true模式
    if 'drn' in [x.node_id for x in task_info.node_graph.all_node_id_set]:
        logger.info('this task contains drn node, it will use ExecutionAlwaysSched')
        task_info.sched_info = ExecutionAlwaysSched()
    return task_info
