import sys
import zipimport
from typing import Protocol, List

from loguru import logger

ENTRY_POINT_MODULE: str = 'app'


class TaskLoaderContext:
    zip_task_path: str


class TaskLoaderError(Exception):
    pass


class TaskLoader(Protocol):
    def task_load(self, task_loader_context: TaskLoaderContext):
        """

        @param task_loader_context:
        @return:
        """
        pass


class ZipTaskLoader:

    @staticmethod
    def task_load(task_loader_context: TaskLoaderContext):
        zip_task_path: str = task_loader_context.zip_task_path
        logger.info(f'start to load task from {zip_task_path}')
        if zip_task_path is None:
            raise TaskLoaderError('load zip task error, the task zip path cannot be blank ')
        sys_path_list: List[str] = sys.path
        if zip_task_path not in sys_path_list:
            sys.path.insert(0, zip_task_path)
            im = zipimport.zipimporter(zip_task_path)
            # 主入口文件都必须放在app.py
            try:
                im.get_filename(ENTRY_POINT_MODULE)
                # 会触发任务主动注册
                im.load_module(ENTRY_POINT_MODULE)
            except:
                raise TaskLoaderError('cannot find the entry module app in the zip!')
        else:
            logger.warning(f'the {zip_task_path} rel task have been loaded before')
