from bottle import request
from Models.SQLhandler import SQLHandler
import json


class weatherController(object):

    def __init__(self):
        self.sqlh = SQLHandler()

    def receive_action(self):
        payload = request.forms.get('payload')
        decoded_payload = json.loads(payload)
        zmienna = []
        for item in decoded_payload:
            zmienna.append(str(item['sensor_id']))
            if item['sensor_id']:
                item['sensor_id_child'] = item.pop('sensor_id')
        self.sqlh.insert('sensor_records', decoded_payload)
        return_payload = self.sqlh.select('select sensor_id_child from sensor_records where sensor_id_child in ({})'.format(', '.join(zmienna)))
        return json.dumps(return_payload)
