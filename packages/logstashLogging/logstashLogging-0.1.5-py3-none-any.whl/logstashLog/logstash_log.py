import json
import logging
import os
import time


# 读取配置文件
def get_config():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)

    # 不断向上查找，直到找到项目根目录（这里假设项目根目录的判断条件是存在config文件夹）
    while not os.path.exists(os.path.join(current_dir, 'config')):
        current_dir = os.path.dirname(current_dir)

    config_file_path = os.path.join(current_dir, 'config', 'log_config.json')

    with open(config_file_path, 'r') as f:
        return json.load(f)
# 获取配置信息并转换为字典类型
config_data = get_config()
service_name = config_data['logging']['service_name']
host = config_data['logging']['host']
port = config_data['logging']['port']


# 日志级别映射
level_mapping = {
    "logging.DEBUG": logging.DEBUG,
    "logging.INFO": logging.INFO,
    "logging.WARNING": logging.WARNING,
    "logging.ERROR": logging.ERROR,
    "logging.CRITICAL": logging.CRITICAL,
}

# 获取配置文件中的日志级别，并判断是否有效
try:
    level_from_config = config_data['logging']['level']
    level = level_mapping.get(level_from_config, logging.INFO)  # 默认值为 logging.INFO
except KeyError:
    level = logging.INFO  # 如果没有找到对应的级别，使用默认值
except KeyError:
    level = logging.INFO

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))

        log_dict = {
            "service_name": service_name,
            "level": record.levelname,
            "message": record.getMessage(),
            "log_time": log_time
        }

        return json.dumps(log_dict)

class CustomTCPLogstashHandler(logstash.TCPLogstashHandler):
    def makePickle(self, record):
        formatted_record = self.formatter.format(record)
        return (formatted_record + '\n').encode('utf-8')  # 确保返回字节串

# 创建日志记录器
test_logger = logging.getLogger('python-logstash-logger')
test_logger.setLevel(level)

# 使用自定义的 TCPLogstashHandler
handler = CustomTCPLogstashHandler(host, port, version=1)
handler.setFormatter(CustomFormatter())
test_logger.addHandler(handler)

# 添加一个StreamHandler用于在控制台打印日志
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
test_logger.addHandler(console_handler)