#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PresentationLayer.PresentationController
import DataLayer.DataController
import LogicLayer.Clock
import EventDispatcher.EventDispatcher
from gi.repository import GObject

def start_gui(event_dispatcher):
    if (event_dispatcher!=None):
        PresentationLayer.PresentationController.initializing(event_dispatcher=event_dispatcher)


class MainLogicController():
    def __init__(self, event_dispatcher=None):
        if (event_dispatcher!=None):
            self.event_dispatcher = event_dispatcher
            self.event_dispatcher.add_event_listener( EventDispatcher.EventDispatcher.MyEvent.GET_ALARM_LIST, self.get_alarm_list)
        self.clock = LogicLayer.Clock.Clock()
        self.last_minute_check = -1
        self.main_screen = PresentationLayer.PresentationController.MainScreenController( event_dispatcher=self.event_dispatcher )
        self._update_id = GObject.timeout_add(1000, self.update_time, None)
        self.data = DataLayer.DataController.MainDataController( event_dispatcher=self.event_dispatcher )

        start_gui(event_dispatcher=self.event_dispatcher) #Start at the end of thread. The process don't back again to this thread

    def update_time(self, extra):
        ## Here the code to check every second
        ## Event for update hour
        self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyEvent (
                        EventDispatcher.EventDispatcher.MyEvent.MAIN_WINDOW_SET_HOUR,
                        self.clock._get_time_formated()
                )
        )

        current_minute = self.clock.get_minutes()
        if (self.last_minute_check != current_minute):
            self.last_minute_check = current_minute
            ## Here the code to check every minute
            self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyEvent (
                        EventDispatcher.EventDispatcher.MyEvent.MAIN_WINDOW_SET_DATE,
                        self.clock.get_date_formated()
                )
            )
        return True
    def get_alarm_list (self, event):
        my_list = self.data.get_alarm_list()
        list_names = []
        for i in my_list:
            list_names.append(i.get_name())

        self.event_dispatcher.dispatch_event(
            EventDispatcher.EventDispatcher.MyEvent ( event.data, list_names )
        )
