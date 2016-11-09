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
            return DataLayer.Alarm.get_alarma_by_name(name)


