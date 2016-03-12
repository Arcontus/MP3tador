#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PresentationLayer.PresentationController
import DataLayer.DataController
import LogicLayer.Clock
from gi.repository import GObject

def start_gui():
    PresentationLayer.PresentationController.initializing()

class MainLogicController():
    def __init__(self):
        self.clock = LogicLayer.Clock.Clock()
        self.last_minute_check = -1
        self.main_screen = PresentationLayer.PresentationController.MainScreenController()
        self._update_id = GObject.timeout_add(1000, self.update_time, None)
        self.data = DataLayer.DataController.MainDataController()

        start_gui() #Start at the end of thread. The process don't back again to this thread

    def update_time(self, extra):
        ## Here the code to check every second
        self.main_screen.set_hour(self.clock._get_time_formated())
        current_minute = self.clock.get_minutes()
        if (self.last_minute_check != current_minute):
            self.last_minute_check = current_minute
            ## Here the code to check every minute
            self.main_screen.set_date(self.clock.get_date_formated())
        return True
