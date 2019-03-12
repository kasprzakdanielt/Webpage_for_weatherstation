from Models.DevicesModel import DevicesModel
from bottle import request


class devicesController(object):

    def devices_action(self):
        x = DevicesModel()
        sensor_names = x.get_all_devices()
        return sensor_names

    def sensors_action(self):
        x = DevicesModel()
        sensor_name_and_type = x.get_sensors()
        return sensor_name_and_type

    def chartdata_action(self):
        x = DevicesModel()
        sensor_name = request.params.device
        sensor_type = request.params.type
        filtering_type = request.params.filtering
        date = x.get_data_for_chart(sensor_name, sensor_type, filtering_type)
        return date
