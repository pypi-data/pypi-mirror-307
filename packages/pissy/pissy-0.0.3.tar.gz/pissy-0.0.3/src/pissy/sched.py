import asyncio
import random

from loguru import logger

from .const import ExecStatus
from .core import TASK_REGISTRY_CENTER, TaskRegistry
from .executions import TaskExecutionInfo

type NodeId = str
type TaskExecutionType = str


class ExecutionOnceSched:

    # noinspection PyMethodMayBeStatic
    def get_task_sched_type(self) -> str:
        return 'exec_once'

    # noinspection PyMethodMayBeStatic
    def get_task_sched_name(self):
        return 'exec_once'

    # noinspection PyMethodMayBeStatic
    async def sched_task_execution(self, task_execution_info: TaskExecutionInfo):
        """
        单次执行
        @param task_execution_info:
        @return:
        """
        logger.info("start to execute task in once policy")
        task_exec_type: TaskExecutionType = task_execution_info.task_info.task_exec_type
        # 获取注册任务
        if task_exec_type not in TASK_REGISTRY_CENTER:
            logger.error("can't find registered task for task_id={}", task_exec_type)
            return
        task_registry: TaskRegistry = TASK_REGISTRY_CENTER[task_exec_type]
        task_func: any = task_registry.func
        # if task_registry.module_name is not None:
        #     task_module: any = __import__(task_registry.module_name)
        # 执行任务
        task_execution_info.curr_task_status = ExecStatus.DING
        task_execution_info.task_execution_dict['execution_round'] = 1
        await task_func(task_execution_info)
        # 任务标记完成
        task_execution_info.curr_task_status = ExecStatus.DONE


class ExecutionAlwaysSched:

    # noinspection PyMethodMayBeStatic
    def get_task_sched_type(self):
        return 'exec_always'

    # noinspection PyMethodMayBeStatic
    def get_task_sched_name(self):
        return 'exec_always'

    # noinspection PyMethodMayBeStatic
    async def sched_task_execution(self, task_execution_info: TaskExecutionInfo):
        """
        always执行
        @param task_execution_info:
        @return:
        """
        task_name: str = task_execution_info.task_info.task_name
        logger.info("start to execute task in always policy")
        init_execution_round: int = 1
        task_execution_info.curr_task_status = ExecStatus.DING
        while True:
            logger.info(f'start to run task={task_name} in the {init_execution_round} round.')
            # 如果当前任务执行状态是STOP退出
            task_status: ExecStatus = task_execution_info.curr_task_status
            if task_status == ExecStatus.DONE:
                logger.info(f'the task={task_name} completed. ')
                break
            task_exec_type: TaskExecutionType = task_execution_info.task_info.task_exec_type
            # 获取注册任务
            if task_exec_type not in TASK_REGISTRY_CENTER:
                logger.error("can't find registered task for task_id={}", task_exec_type)
                return
            task_registry: TaskRegistry = TASK_REGISTRY_CENTER[task_exec_type]
            task_func: any = task_registry.func
            # if task_registry.module_name is not None:
            #     task_module: any = __import__(task_registry.module_name)
            # 执行任务
            # task_execution_info.curr_task_status = ExecStatus.DING
            task_execution_info.task_execution_dict['execution_round'] = init_execution_round
            await task_func(task_execution_info)
            init_execution_round = init_execution_round + 1
            # 随机sleep一段时间
            sleep_time_in_seconds: float = random.random()
            await asyncio.sleep(sleep_time_in_seconds)
