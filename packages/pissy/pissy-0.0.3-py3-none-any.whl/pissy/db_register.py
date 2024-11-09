import inspect
import threading

from loguru import logger
from sqlalchemy import Engine, create_engine

register_lock = threading.Lock()

DB_REGISTER: dict[str, Engine] = {}


def register_db(db_sign: str, db_config: dict[str, any]) -> None:
    """
    register db
    dialect[+driver]://user:password@host/dbname[?key=value..];sqlite,mysql+pymysql, oracle+cx_oracle
    @param db_sign:
    @param db_config:url and other db params
    @return:
    """
    with register_lock:
        if db_sign in DB_REGISTER:
            return
        if 'url' not in db_config:
            return
        curr_db_engine: Engine = create_engine(**db_config)
        DB_REGISTER[db_sign] = curr_db_engine


def get_db(db_sign: str) -> Engine | None:
    """
    fetched node related db
    @param db_sign:
    @return:
    """
    fetched_db_engine: Engine | None = DB_REGISTER.get(db_sign, None)
    if fetched_db_engine is None:
        logger.error(f"the {db_sign} related datasource haven't been initialized!")
        return None
    return fetched_db_engine
