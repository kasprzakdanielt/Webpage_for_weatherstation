from __future__ import division
from Models.SQLhandler import SQLHandler
import pandas as pd


class DevicesModel(object):

    def __init__(self):
        self.sqlh = SQLHandler()

    def get_all_devices(self):
        sensor_names = self.sqlh.select("SELECT distinct sensor_name FROM sensor_records order by sensor_name")
        return sensor_names

    def get_sensors(self):
        sensor_names = self.get_all_devices()
        sensor_name_and_type = []
        for sensor_name in sensor_names:
            sensor_name_and_type.append(sensor_name)
            sensor_type = self.sqlh.select(
                "SELECT distinct sensor_type FROM sensor_records where sensor_name = '{}'".format(
                    sensor_name['sensor_name']))
            sensor_name['sensor_types'] = []
            for sensor_types in sensor_type:
                sensor_name['sensor_types'].append(sensor_types['sensor_type'])
        return sensor_name_and_type

    def get_data_for_chart(self, sensor_name, sensor_type, filtering):
        chart_data = None
        value = []
        date = []

        if filtering == 'hour':
            chart_data = self.get_data_from_last_hour(sensor_name, sensor_type)
        if filtering == 'day':
            chart_data = self.get_data_from_last_day(sensor_name, sensor_type)
        if filtering == 'month':
            date, value = self.get_data_from_last_month(sensor_name, sensor_type)



        for idx in chart_data:
            value.append(idx["sensor_data"])
            date.append(idx["sensor_date"])
        max_value = float(max(value)) + 1
        min_value = float(min(value)) - 1
        return date, value, int(round(max_value)), int(round(min_value))

    def get_data_from_last_hour(self, sensor_name, sensor_type):
        chart_data = self.sqlh.select(
            "select sensor_date, sensor_data from sensor_records where sensor_name = '{}' and sensor_type= '{}' and sensor_date >= datetime('now', '-1 hours') order by sensor_date".format(
                sensor_name, sensor_type))
        return chart_data

    def get_data_from_last_day(self, sensor_name, sensor_type):
        chart_data = self.sqlh.select(
            "select sensor_date, sensor_data from sensor_records where sensor_name = '{}' and sensor_type= '{}' and sensor_date >= datetime('now', '-1 day') order by sensor_date".format(
                sensor_name, sensor_type))

        return chart_data

    # to nie dziala, zwraca zly typ
    def get_data_from_last_month(self, sensor_name, sensor_type):
        data = self.sqlh.select(
            "select sensor_date, sensor_data from sensor_records where sensor_name = '{}' and sensor_type= '{}' and sensor_date >= datetime('now', '-1 month') order by sensor_date".format(
                sensor_name, sensor_type))
        dataframe = pd.DataFrame.from_records(data)
        dataframe['sensor_date'] = pd.to_datetime(dataframe['sensor_date'])
        dataframe['sensor_date'] = dataframe['sensor_date'].apply(lambda x: x.date())
        dataframe['sensor_data'] = dataframe['sensor_data'].astype('float')

        # tutaj mam dataframe i spoko

        dataframe_avg = dataframe.groupby('sensor_date')['sensor_data'].mean()
        # tutaj juz nie jest niby dataframe i juz nie spoko :|

        # dataframe.to_dict()

        return self.turn_dataframe_back_to_list_of_dicts(dataframe_avg)

    def turn_dataframe_back_to_list_of_dicts(self, dataframe_avg):
        # to ma byc funkcja do zamiany tego czegos wczesniej na to co mi potrzeba czyli listy dictow
        # print dataframe_avg
        #print dataframe_avg.
        wartosci = dataframe_avg.tolist()
        daty = dataframe_avg.index.get_values()
        print (type(daty))
        print (wartosci)
        print (daty)
        return daty, wartosci
