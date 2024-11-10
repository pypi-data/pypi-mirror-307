from enum import Enum, auto


class TaskExecType(Enum):
    LOCAL = auto()


class ExecStatus(Enum):
    DING = 'ding'
    DONE = 'done'
    WAIT = 'wait'


class DbVars(Enum):
    PAGE_SIZE = 'page_size'
    PAGE_IDX = 'page_index'
    PAGE_OFFSET = 'page_offset'
    FROM_TABLE = 'from_table'
    TO_TABLE = 'to_table'
    ORDER_BY_COND = 'order_by'
    INCR_KEY = 'incr_key'
    INCR_KEY_VALUE = 'incr_key_value'
    COLUMNS = 'columns'


DB_REF_KEY_SUFFIX = '_db'
KAFKA_KEY_SUFFIX = '_kafka'
