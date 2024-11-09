import asyncio
import importlib.abc
import time
from typing import Annotated, Union

import typer
from loguru import logger

from .const import ExecStatus
from .executions import TaskSched, TaskExecutionInfo
from .task import TaskInfo
from .task_config_loader import create_task_from_json
from .task_config_validator import validate_task_config_json
from .task_loader import TaskLoader, ZipTaskLoader, TaskLoaderContext

# from .dbms_core import RdbmsWriterNode,RdbmsReaderNode

app = typer.Typer(
    help='pissy是一个支持数据节点同步工具',
    # 隐藏--install-completion 命令
    add_completion=False,
)


# noinspection PyUnresolvedReferences
@app.command()
def start(config: Annotated[typer.FileText, typer.Option('--config', '-c', help='任务配置描述,需要是json格式')],
          path: str = typer.Option(None, '--path', '-p', help='自定义zip包时,需要指定包的位置,启动模块需要是app')):
    """
    @param path:
    @param config:
    @return:
    """
    task_config_json: str = config.read()
    # typer.echo(f'任务配置:{task_config_json}')
    start_task(task_config=task_config_json, task_path=path)
    # typer.echo('任务执行完成')


def start_task(task_config: str, task_path: str = None):
    """

    @param task_config:
    @param task_path:
    @return:
    """
    # 手工加载需要的模块
    importlib.import_module('pissy.dbms_core')
    importlib.import_module('pissy.kafka_core')
    error_msg: Union[str | None] = validate_task_config_json(task_config_json=task_config)
    if error_msg is not None:
        typer.echo(error_msg)
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


def main():
    app()
