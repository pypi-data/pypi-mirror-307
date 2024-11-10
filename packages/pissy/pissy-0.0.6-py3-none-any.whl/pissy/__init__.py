import logging.config
import os.path

# 加载日志配置,模块被加载，大家共享相同的配置
# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建配置文件的相对路径
config_path = os.path.join(current_dir, 'logger.conf')
# 不加disable_existing_loggers=False 可能导致部分模块日志不打印
logging.config.fileConfig(config_path, disable_existing_loggers=False)
