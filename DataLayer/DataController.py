"""
Manage all things about the data and files and exposes some public functions for using on
LogicController.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "David Pozos Ceron"

import DataLayer.Library
import DataLayer.Alarm


class MainDataController:
    def __init__(self, event_dispatcher=None):
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher
        DataLayer.Library.load_library_list()
        DataLayer.Alarm.load_alarm_list()

    @staticmethod
    def get_alarm_list():
        return DataLayer.Alarm.get_alarm_list()

    @staticmethod
    def get_library_list():
        return DataLayer.Library.get_library_list()

    @staticmethod
    def get_alarm(name):
        if name is None:
            return None
        else:
            return DataLayer.Alarm.get_alarm_by_name(name)

    @staticmethod
    def save_alarm(alarm_dict):
        add_alarm = False
        my_alarm = DataLayer.Alarm.get_alarm_by_name(alarm_dict['name'])
        if not my_alarm:
            my_alarm = DataLayer.Alarm.Alarm()
            add_alarm = True
        my_alarm.set_name(alarm_dict['name'])
        my_alarm.set_active(alarm_dict['active'])
        my_alarm.set_days(alarm_dict['days'])
        my_alarm.set_monday(alarm_dict['monday'])
        my_alarm.set_tuesday(alarm_dict['tuesday'])
        my_alarm.set_wednesday(alarm_dict['wednesday'])
        my_alarm.set_thursday(alarm_dict['thursday'])
        my_alarm.set_friday(alarm_dict['friday'])
        my_alarm.set_saturday(alarm_dict['saturday'])
        my_alarm.set_sunday(alarm_dict['sunday'])
        my_alarm.set_hours(alarm_dict['hours'])
        my_alarm.set_minutes(alarm_dict['minutes'])
        my_alarm.set_library(alarm_dict['library'])
        my_alarm.set_snooze(alarm_dict['snooze'])
        my_alarm.set_min_snooze(alarm_dict['min_snooze'])
        my_alarm.save_params()
        if add_alarm:
            DataLayer.Alarm.add_alarm(my_alarm)
            return True
        else:
            return False


