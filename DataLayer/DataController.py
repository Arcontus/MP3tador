#!/usr/bin/env python
# -*- coding: utf-8 -*-

import DataLayer.Library
import DataLayer.Alarm
import EventDispatcher.EventDispatcher


class MainDataController:
    def __init__(self, event_dispatcher=None):
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher
        DataLayer.Library.load_library_list()
        DataLayer.Alarm.load_alarm_list()

    def get_alarm_list(self):
        return DataLayer.Alarm.get_alarm_list()

    def get_library_list(self):
        return DataLayer.Library.get_library_list()


