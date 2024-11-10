import asyncio
import importlib.abc
import logging
import sys
import time
from typing import Union

from pissy.const import ExecStatus
from pissy.executions import TaskSched, TaskExecutionInfo
from pissy.task import TaskInfo
from pissy.task_config_loader import create_task_from_json
from pissy.task_config_validator import validate_task_config_json
from pissy.task_loader import TaskLoader, ZipTaskLoader, TaskLoaderContext

logger = logging.getLogger(__name__)


def command(args):
    with open(args.config) as file:
        task_config_json = file.read()
    logger.info(f'task config: {task_config_json}')
    try:
        start_task(task_config=task_config_json, task_path=args.zip, lib_path=args.lib)
    except Exception as ex:
        logger.error(f'start error throws ex. {ex.__str__()}', )


def start_task(task_config: str, task_path: str = None, lib_path: str = None):
    """

    @param task_config: 任务配置json格式
    @param task_path: 自定义zip包格式任务
    @param lib_path: 自定义zip包时第三方lib目录,可能时site-packages
    @return:
    """
    if lib_path is not None:
        # 注册module path
        if lib_path not in sys.path:
            sys.path.insert(-1, lib_path)
    # 手工加载需要的模块
    importlib.import_module('pissy.extensions.dbms.dbms_core')
    importlib.import_module('pissy.extensions.kafka.kafka_core')
    error_msg: Union[str | None] = validate_task_config_json(task_config_json=task_config)
    if error_msg is not None:
        logger.info(error_msg)
        return
    # 加载zip包版本的zip task
    if task_path is not None:
        logger.info(f"load zip task from {task_path}")
        task_loader: TaskLoader = ZipTaskLoader()
        task_loader_context: TaskLoaderContext = TaskLoaderContext()
        task_loader_context.zip_task_path = task_path
        task_loader.task_load(task_loader_context)
    # 校验任务json配置
    # 注册内置的节点列表
    # init task
    curr_t: TaskInfo = create_task_from_json(task_config_json=task_config)
    if curr_t is None:
        logger.error(f'init task failed!')
        return
    # start task
    task_binding_sched: TaskSched = curr_t.sched_info
    task_execution_info: TaskExecutionInfo = TaskExecutionInfo()
    task_execution_info.task_info = curr_t
    task_execution_info.curr_task_status = ExecStatus.WAIT
    task_execution_info.start_time = time.time()
    asyncio.run(task_binding_sched.sched_task_execution(task_execution_info))
    task_execution_info.stop_time = time.time()
