import json
from json import JSONDecodeError
from typing import Union

from jsonschema import validate, ValidationError

task_config_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Task Configuration",
    "description": "A task configuration schema",
    "properties": {
        "task_name": {
            "type": "string",
            "description": "任务名称"
        },
        "nodes": {
            "type": "string",
            "description": "任务间节点关系图;比如A依赖B我们写成A->B多组关系用;分割,"
        },
        "datasource": {
            "type": "object",
            "description": "The datasource configuration.",
            "patternProperties": {
                "^.*$": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "sqlalchemy 格式的数据库连接串"
                        }
                    },
                    "required": ["url"]
                }
            },
            "additionalProperties": False
        },
        "kafka": {
            "type": "object",
            "patternProperties": {
                "^.*$": {
                    "type": "object",
                    "properties": {
                        "bootstrap_servers": {
                            "type": "string",
                            "description": "kafka server地址列表"
                        }
                    },
                    "required": ["bootstrap_servers"]
                }
            },
        },
        "drn": {
            "type": "object",
            "description": "the db reader node config",
            "properties": {
                "from_db": {
                    "type": "string",
                    "description": "引用的上面datasource里面的哪个db"
                },
                "from_table": {
                    "type": "string",
                    "description": "源表"
                },
                "incr_key": {
                    "type": "string",
                    "description": "增量键,一般用时间"
                },
                "incr_key_value": {
                    "type": "string",
                    "description": "增量键值"
                },
                "page_size": {
                    "type": "integer",
                    "description": "一次读取多少条"
                },
                "sql_template": {
                    "type": "string",
                    "description": "支持自定义sql加载数据"
                }
            },
            "required": ["from_db", "from_table", "incr_key", "incr_key_value", "page_size", "sql_template"]
        },
        "dwn": {
            "type": "object",
            "description": "the db writer node",
            "properties": {
                "to_db": {
                    "type": "string",
                    "description": "引用的上面datasource里面的哪个db"
                },
                "to_table": {
                    "type": "string",
                    "description": "目标表"
                }
            },
            "required": ["to_db", "to_table"]
        },
        "ffk": {
            "type": "object",
            "description": "从kafka加载数据节点",
            "properties": {
                "from_kafka": {
                    "type": "string",
                    "description": "引用上面的kafka中的哪个kafka"
                },
                "topic": {
                    "type": "string",
                    "description": "消费哪个kafka"
                },
            },
            "required": ["from_kafka", "topic"]
        }
    },
    "required": ["task_name", "nodes", ]
}


def validate_task_config_json(task_config_json: str) -> Union[str | None]:
    try:
        task_config_dict = json.loads(task_config_json)
    except JSONDecodeError as ex:
        return f'not a valid json format,error:{ex.msg}'
    try:
        validate(task_config_dict, schema=task_config_schema)
    except ValidationError as ex:
        return ex.message
    return None
