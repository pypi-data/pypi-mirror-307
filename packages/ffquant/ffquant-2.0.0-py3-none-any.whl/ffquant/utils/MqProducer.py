from datetime import datetime
import json
from confluent_kafka import Producer

__ALL__ = ['MqProducer']

class MqProducer():
    def __init__(self, *args, **kwargs):
        conf = {
            'bootstrap.servers': '192.168.25.148:9092',
            'client.id': f"MqProducer_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
        self.producer = Producer(conf)

    def start(self):
        pass

    def send(self, symbol="", type_name="", millis=0, data=None):
        # (time_open),(time_close),(type),(symbol),(signal_key),(signal_value)
        value = f"{millis}|{millis + 60 * 1000}|{str(type_name).replace('|', '_')}|{str(symbol).replace('|', '_')}|data|{json.dumps({'data': data}).replace('|', '_')}"
        self.producer.produce("t_index_info_data", key="", value=value)
        self.producer.flush()