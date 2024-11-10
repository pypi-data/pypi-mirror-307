from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, List

from .const import DbVars


@runtime_checkable
class Dialect(Protocol):

    def render_read_sql(self, db_vars: dict[str, any]) -> str:
        """
        获取增量读取sql
        @param db_vars:
        @return:
        """
        pass

    def render_batch_writer_sql(self, db_vars: dict[str, any]) -> str:
        """
        获取批量写入sql
        @param db_vars:
        @return:
        """
        pass


class BaseDialect(ABC, Dialect):

    @abstractmethod
    def get_page_reader_sql_template(self, db_vars: dict[str, any]) -> str:
        pass

    def render_read_sql(self, db_vars: dict[str, any]) -> str:
        return self.get_page_reader_sql_template(db_vars=db_vars).format(**db_vars)

    @abstractmethod
    def get_batch_writer_template(self, db_vars: dict[str, any]) -> str:
        pass

    def render_batch_writer_sql(self, db_vars: dict[str, any]) -> str:
        return self.get_batch_writer_template(db_vars=db_vars).format(**db_vars)


class OracleDialect(BaseDialect):

    def get_page_reader_sql_template(self, db_vars: dict[str, any]) -> str:
        order_by_cond: str | None = db_vars.get(DbVars.ORDER_BY_COND.value, None)
        if order_by_cond is None or len(order_by_cond) == 0:
            order_by_cond = ''
        else:
            order_by_cond = f' order by {order_by_cond}'
        # 如果没有配置增量键,走full table读取
        filter_cond = f'where {{{DbVars.INCR_KEY.value}}} >= {{{DbVars.INCR_KEY_VALUE.value}}}'
        if db_vars.get(DbVars.INCR_KEY.value, None) is None:
            filter_cond = 'where 1=1'
        filter_page_sql: str = f"""
        SELECT * FROM {{{DbVars.FROM_TABLE.value}}} {filter_cond} {order_by_cond}
        OFFSET {{{DbVars.PAGE_OFFSET.value}}} ROWS FETCH NEXT {{{DbVars.PAGE_SIZE.value}}} ROWS ONLY
        """
        return filter_page_sql

    def get_batch_writer_template(self, db_vars: dict[str, any]) -> str:
        """
        暂不考虑支持merge into
        @param db_vars:
        @return:
        """
        column_names: List[str] = db_vars.get(DbVars.COLUMNS.value)
        column_names_part: str = '(' + ','.join(column_names) + ')'
        column_placeholder_part: str = '(' + ','.join(['%s' for _ in range(len(column_names))]) + ')'
        return f"""
        insert into  
        {{{DbVars.TO_TABLE.value}}} 
        {column_names_part} 
        values  
        {column_placeholder_part}
        """


class MysqlDialect(BaseDialect):

    def get_page_reader_sql_template(self, db_vars: dict[str, any]) -> str:
        """
        @return:
        """
        order_by_cond: str | None = db_vars.get(DbVars.ORDER_BY_COND.value, None)
        if order_by_cond is None or len(order_by_cond) == 0:
            order_by_cond = ''
        else:
            order_by_cond = f' order by {order_by_cond}'
        filter_cond = f'{{{DbVars.INCR_KEY.value}}} >= {{{DbVars.INCR_KEY_VALUE.value}}}'
        if db_vars.get(DbVars.INCR_KEY.value, None) is None:
            filter_cond = ' 1=1 '
        filter_page_sql: str = f"""
        select * from 
        {{{DbVars.FROM_TABLE.value}}} 
        where  {filter_cond} {order_by_cond}
        limit {{{DbVars.PAGE_OFFSET.value}}}, {{{DbVars.PAGE_SIZE.value}}}
        """
        return filter_page_sql

    def get_batch_writer_template(self, db_vars: dict[str, any]) -> str:
        """
        REPLACE INTO employees (id, name, department)
        VALUES (1, 'John Doe', 'Sales');
        @return:
        """
        column_names: List[str] = db_vars.get(DbVars.COLUMNS.value)
        column_names_part: str = '(' + ','.join(column_names) + ')'
        column_placeholder_part: str = '(' + ','.join(['%s' for _ in range(len(column_names))]) + ')'
        return f"""
        replace into  
        {{{DbVars.TO_TABLE.value}}} 
        {column_names_part} 
        values  
        {column_placeholder_part}
        """


class SqliteDialect(MysqlDialect):

    def get_batch_writer_template(self, db_vars: dict[str, any]) -> str:
        return super().get_batch_writer_template(db_vars).replace('%s', '?')


class InvalidDbSignError(Exception):
    pass


def get_db_dialect(db_sign: str) -> Dialect:
    """
    @param db_sign:
    @return:
    """
    if db_sign is None:
        raise InvalidDbSignError("db_sign is empty!")
    if db_sign.lower() in ['mysql']:
        return MysqlDialect()
    if db_sign.lower() in ['sqlite']:
        return SqliteDialect()
    if db_sign.lower() in ['oracle']:
        return OracleDialect()
    raise InvalidDbSignError(f"current db_sign={db_sign} is supported!")
