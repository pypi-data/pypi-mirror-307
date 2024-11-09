import threading
from typing import Union

from kafka import KafkaClient, KafkaConsumer
from loguru import logger

KAFKA_REGISTER: dict[str, KafkaConsumer] = {}
kafka_register_lock = threading.Lock()


def register_kafka(kafka_sign: str, kafka_config: dict[str, any]) -> None:
    """
    @param kafka_sign:
    @param kafka_config:
    @return:
    """
    with kafka_register_lock:
        if kafka_sign is None or len(kafka_sign) == 0:
            logger.error('the kafka_sign is empty!')
            return
        if kafka_sign in KAFKA_REGISTER:
            logger.warning('the kafka_sign related kafka have been registered.')
            return
        kafka_consumer: KafkaConsumer = KafkaConsumer(**kafka_config)
        KAFKA_REGISTER[kafka_sign] = kafka_consumer


def get_kafka(kafka_sign: str) -> Union[KafkaClient | None]:
    """
    @param kafka_sign:
    @return:
    """
    if kafka_sign is None or len(kafka_sign) == 0:
        return None
    return KAFKA_REGISTER.get(kafka_sign, None)
