from dataclasses import dataclass
from typing import List, AnyStr

from loguru import logger
from sqlalchemy import text, Engine, CursorResult, TextClause

from .const import DbVars, ExecStatus
from .core import task_node
from .executions import TaskNodeExecutionInfo
from .dialect import Dialect, get_db_dialect
from .dbms_models import MultiRows, ColumnField


@dataclass
class RdmsReaderNodeParam:
    binding_datasource: Engine


class RdbmsReaderNode:
    __db_sign: str
    __db_dialect: Dialect
    __sql_template: AnyStr | None

    def __parse_params(self, node_param_dict: dict[str, any]):
        """
        @param node_param_dict:
        @return:
        """
        self.__db_sign = node_param_dict.get('from_db').name
        self.__db_dialect = get_db_dialect(db_sign=self.__db_sign)
        self.__sql_template = node_param_dict.get('sql_template', '')

    # @logger.catch()
    def read_rows(self, task_node_execution: TaskNodeExecutionInfo) -> MultiRows:
        """
        执行数据读取
        @param task_node_execution:
        @return:
        """
        # 获取执行参数
        node_param_dict: dict[str, any] = task_node_execution.node_param_dict
        self.__parse_params(node_param_dict=node_param_dict)
        task_execution_dict: dict[str, any] = task_node_execution.task_execution_info.task_execution_dict
        node_param: RdmsReaderNodeParam = RdmsReaderNodeParam(node_param_dict.get('from_db'))
        binding_datasource: Engine = node_param.binding_datasource
        # 获取column列表
        column_fields: List[ColumnField] = task_execution_dict.get('column.fields', [])
        # 执行sql渲染,生成执行sql
        render_sql_params: dict[str, any] = self.__get_render_sql_params(task_node_execution=task_node_execution)
        reader_sql: str = self.__get_reader_sql(render_sql_params=render_sql_params)
        # 执行sql 脚本
        reader_sql_statement: TextClause = text(reader_sql)
        logger.info(f"reader sql: {reader_sql_statement}")

        with binding_datasource.connect() as curr_conn:
            curr_cursor: CursorResult[any] = curr_conn.execute(reader_sql_statement)
            # 提取列信息
            if column_fields is None or len(column_fields) == 0:
                column_fields = column_fields + [ColumnField(columnName=column_name, sqlType=0) for column_name in
                                                 curr_cursor.keys()]
                task_execution_dict['column_fields'] = column_fields

            # 解析结果
            curr_multi_rows: MultiRows = MultiRows(column_list=column_fields)
            for row_value_tuple in curr_cursor:
                curr_multi_rows.add_row(row=list(row_value_tuple))
            logger.info(f'drn node get {curr_multi_rows.get_rows_len()} rows from db.')
            return curr_multi_rows

    @staticmethod
    def __get_render_sql_params(task_node_execution: TaskNodeExecutionInfo) -> dict[str, any]:
        """
        get render sql that needs
        @param task_node_execution:
        @return:
        """
        node_param_dict: dict[str, any] = task_node_execution.node_param_dict
        r: dict[str, any] = {DbVars.FROM_TABLE.value: node_param_dict.get(DbVars.FROM_TABLE.value, ''),
                             DbVars.INCR_KEY.value: node_param_dict.get(DbVars.INCR_KEY.value, ''),
                             DbVars.INCR_KEY_VALUE.value: node_param_dict.get(DbVars.INCR_KEY_VALUE.value, ''),
                             DbVars.ORDER_BY_COND.value: node_param_dict.get(DbVars.ORDER_BY_COND.value, ''),
                             DbVars.PAGE_SIZE.value: node_param_dict.get(DbVars.PAGE_SIZE.value, ''), }
        # round参数从执行上下文中取
        task_execution_dict: dict[str, any] = task_node_execution.task_execution_info.task_execution_dict
        curr_round: int = task_execution_dict.get('execution_round', 1)
        page_offset: int = (curr_round - 1) * r[DbVars.PAGE_SIZE.value]
        r[DbVars.PAGE_OFFSET.value] = page_offset
        return r

    def __get_reader_sql(self, render_sql_params: dict[str, any]):
        if self.__sql_template is None or len(self.__sql_template) == 0:
            return self.__db_dialect.render_read_sql(render_sql_params)
        return self.__sql_template.format(**render_sql_params)


@dataclass()
class RdmsWriterNodeParam:
    binding_datasource: Engine


class RdbmsWriterNode:
    __db_sign: str
    __db_dialect: Dialect

    def __parse_params(self, node_param_dict: dict[str, any]):
        """

        @param node_param_dict:
        @return:
        """
        self.__db_sign = node_param_dict.get('to_db').name
        self.__db_dialect = get_db_dialect(db_sign=self.__db_sign)

    # @logger.catch()
    def write_rows(self, task_node_execution: TaskNodeExecutionInfo) -> None:
        """
        执行数据写入
        :param task_node_execution:
        :return:
        """
        # 获取上次执行结果
        node_param_dict: dict[str, any] = task_node_execution.node_param_dict
        self.__parse_params(node_param_dict=node_param_dict)
        node_param: RdmsReaderNodeParam = RdmsReaderNodeParam(node_param_dict.get('to_db'))
        binding_datasource: Engine = node_param.binding_datasource
        node_result_dict: dict[str, any] = task_node_execution.node_result_dict
        # noinspection PyTypeChecker
        multi_rows: MultiRows = node_result_dict.get('drn', None)
        if multi_rows is None or multi_rows.get_rows_len() == 0:
            logger.info("there is no rows need to insert, quit.")
            task_node_execution.task_execution_info.curr_task_status = ExecStatus.DONE
            return None
        logger.info(f'dwn node start to write {multi_rows.get_rows_len()} rows to db')
        # 执行sql渲染,生成执行sql
        render_sql_params: dict[str, any] = self.__get_render_sql_params(task_node_execution=task_node_execution)
        writer_sql: str = self.__get_write_sql(render_sql_params=render_sql_params)
        # 使用原生的executemany
        logger.info(f'writer sql: {writer_sql}')
        curr_conn = None
        curr_cursor = None
        try:
            curr_conn = binding_datasource.raw_connection()
            curr_cursor = curr_conn.cursor()
            params_lst = [list(tmp_row) for tmp_row in multi_rows]
            curr_cursor.executemany(writer_sql, params_lst)
            curr_conn.commit()
        finally:
            if curr_cursor is not None:
                curr_cursor.close()
            if curr_conn is not None:
                curr_conn.close()

    @staticmethod
    def __get_render_sql_params(task_node_execution: TaskNodeExecutionInfo) -> dict[str, any]:
        """

        :param task_node_execution:
        :return:
        """
        task_node_param: dict[str, any] = task_node_execution.node_param_dict
        r: dict[str, any] = {}
        column_fields: List[ColumnField] = task_node_execution.task_execution_info.task_execution_dict.get(
            'column_fields', [])
        r[DbVars.COLUMNS.value] = [it.columnName for it in column_fields]
        r[DbVars.TO_TABLE.value] = task_node_param.get(DbVars.TO_TABLE.value, '')
        return r

    def __get_write_sql(self, render_sql_params: dict[str, any]):
        """

        :param render_sql_params:
        :return:
        """
        return self.__db_dialect.render_batch_writer_sql(render_sql_params)


reader_node: RdbmsReaderNode = RdbmsReaderNode()
writer_node: RdbmsWriterNode = RdbmsWriterNode()


# noinspection PyBroadException
@task_node(node_id='drn', dep_on=[])
async def do_read(task_node_execution_info: TaskNodeExecutionInfo) -> MultiRows:
    """

    @param task_node_execution_info:
    @return:
    """
    try:
        reader_result: MultiRows = reader_node.read_rows(task_node_execution=task_node_execution_info)
        if reader_result.get_rows_len() == 0:
            task_node_execution_info.task_execution_info.curr_task_status = ExecStatus.DONE
        return reader_result
    except Exception as ex:
        logger.error(f'execute db_reader_node=drn throws ex, error message:{ex}')
        raise ex


@task_node(node_id='dwn', dep_on=['DRN'])
async def do_write(task_node_execution_info: TaskNodeExecutionInfo) -> None:
    """

    @param task_node_execution_info:
    @return:
    """
    try:
        writer_node.write_rows(task_node_execution=task_node_execution_info)
        return None
    except Exception as ex:
        logger.error(f"execute db_writer_node=dwn throws ex, error message:{ex}")
        raise ex
