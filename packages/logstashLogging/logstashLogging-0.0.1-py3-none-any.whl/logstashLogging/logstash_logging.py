import json
import logging
import time
import logstash

# 读取配置文件
with open('config/log_config.json', 'r') as f:  # 使用相对路径
    config = json.load(f)
service_name = config['logging']['service_name']
host = config['logging']['host']
port = config['logging']['port']
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))

        log_dict = {
            "service_name": service_name,
            "log_level": record.levelname,
            "log_message": record.getMessage(),
            "log_time": log_time
        }

        return json.dumps(log_dict)

class CustomTCPLogstashHandler(logstash.TCPLogstashHandler):
    def makePickle(self, record):
        formatted_record = self.formatter.format(record)
        return (formatted_record + '\n').encode('utf-8')  # 确保返回字节串

# 创建日志记录器
test_logger = logging.getLogger('python-logstash-logger')
test_logger.setLevel(logging.DEBUG)

# 使用自定义的 TCPLogstashHandler
handler = CustomTCPLogstashHandler(host, port, version=1)
handler.setFormatter(CustomFormatter())
test_logger.addHandler(handler)
