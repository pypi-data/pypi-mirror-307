import uuid
from typing import Protocol

from .const import ExecStatus
from .task import TaskInfo, NodeId


class TaskExecutionInfo(object):
    task_execution_id: str = uuid.uuid1()
    task_info: TaskInfo
    start_time: float
    stop_time: float
    curr_task_status: ExecStatus.WAIT
    task_param_dict: dict[str, any] = {}
    # 执行上下文,临时变量区
    task_execution_dict: dict[str, any] = {}


class TaskNodeExecutionInfo(object):
    task_node_execution_id: str = uuid.uuid1()
    task_execution_info: TaskExecutionInfo
    node_id: NodeId
    curr_task_node_status: ExecStatus.WAIT
    # 节点执行要的参数,初始化用
    node_param_dict: dict[str, any] = {}
    # 依赖节点的执行结果
    node_result_dict: dict[str, any] = {}
    # 执行上下文,临时变量区
    node_execution_dict: dict[str, any] = {}
    start_time: float
    stop_time: float


class TaskSched(Protocol):
    def get_task_sched_type(self):
        pass

    def get_task_sched_name(self):
        pass

    async def sched_task_execution(self, task_execution_info: TaskExecutionInfo):
        pass
