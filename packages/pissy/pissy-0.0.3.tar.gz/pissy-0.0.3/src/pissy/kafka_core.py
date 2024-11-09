from kafka import KafkaConsumer
from loguru import logger

from pissy.core import task_node
from pissy.executions import TaskNodeExecutionInfo


@task_node(node_id='ffk')
async def fetch_from_kafka(task_node_execution_info: TaskNodeExecutionInfo) -> any:
    """
    从kafka中获取数据
    @param task_node_execution_info:
    @return:
    """
    node_param_dict: dict[str, any] = task_node_execution_info.node_param_dict
    kafka_consumer: KafkaConsumer = node_param_dict.get('from_kafka')
    curr_topic: str = node_param_dict.get('topic')
    if curr_topic is None or len(curr_topic) == 0:
        logger.error('the consumer topic should be specified.')
        return None
    # 订阅kafka
    if curr_topic not in kafka_consumer.topics():
        kafka_consumer.subscribe(list(curr_topic), )
    messages = kafka_consumer.poll(max_records=100)
    # 处理拉取到的消息
    # for message in messages:
    #     if message is not None:
    #         print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
    return list([message.value for message in messages])
