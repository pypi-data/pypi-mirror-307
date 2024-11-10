import argparse
import logging.config
import sys

from .commands.demo_config_command import command as demo
from .commands.start_task_command import command as start

logger = logging.getLogger(__name__)


def main():
    # 必须有启动命令
    if len(sys.argv[1:]) < 1:
        print('usage: pissy [-h] {start} ...')
        sys.exit(1)
    parser = argparse.ArgumentParser(description='pissy是一个支持数据节点同步工具')
    sub_parsers = parser.add_subparsers(help='命令列表')
    # 注册start命令
    start_command = sub_parsers.add_parser('start', help='启动任务命令')
    start_command.add_argument('--config', '-c', type=str, help='任务配置描述,需要是json格式', required=True)
    start_command.add_argument('--zip', '-z', help='自定义zip包时,需要指定包的位置,启动模块需要是app', required=False)
    start_command.add_argument('--lib', '-l', help='第三方lib目录', required=False)
    start_command.set_defaults(func=lambda args: start(args=args))

    # 注册demo命令
    demo_command = sub_parsers.add_parser('demo', help='获取任务同步json demo,提供的是一个数据库同步示例')
    demo_command.set_defaults(func=lambda args: demo(args=args))
    args = parser.parse_args()
    args.func(args)
