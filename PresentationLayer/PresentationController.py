#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import PresentationLayer.Main
import PresentationLayer.Library
import PresentationLayer.Alarm
import PresentationLayer.Option
import EventDispatcher.EventDispatcher

def start_gui():
    win = PresentationLayer.Main.MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class MainScreenController(Borg):
    def __init__(self, main_window=None , event_dispatcher=None):
        Borg.__init__(self)
        if (main_window != None):
            self.window = main_window
        if (event_dispatcher != None):
            self.event_dispatcher=event_dispatcher
            self.event_dispatcher.add_event_listener( EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_HOUR, self.set_hour)
            self.event_dispatcher.add_event_listener( EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_DATE, self.set_date)

    def openLibraryManager(self):
        self.my_library = PresentationLayer.Library.LibraryManagerWindow()
        self.my_library.show_all()

    def openAlarmManager(self):
        self.my_alarm = PresentationLayer.Alarm.AlarmManager()
        self.my_alarm.show_all()

    def openOptionManager(self):
        self.my_option = PresentationLayer.Option.OptionWindow()
        self.my_option.show_all()

    def set_hour(self, hour):
        self.window.set_hour(hour)

    def set_date(self, date):
        self.window.set_date(date)

class AlarmScreenController():
    def __init__(self, event_dispatcher=None):
        if (event_dispatcher != None):
            self.event_dispatcher=event_dispatcher
            self.event_dispatcher.add_event_listener( EventDispatcher.EventDispatcher.MyAlarmEvent.SET_ALARM_LIST, self.reload_items)
        self.window = PresentationLayer.Alarm.AlarmManager(self)
        self.get_items()
        self.window.show_all()

    def get_items(self):
        self.event_dispatcher.dispatch_event(
            EventDispatcher.EventDispatcher.MyAlarmEvent ( EventDispatcher.EventDispatcher.MyAlarmEvent.GET_ALARM_LIST, EventDispatcher.EventDispatcher.MyAlarmEvent.SET_ALARM_LIST )
        )
    def reload_items(self, event):
        self.window.reload_items(event)

    def openAlarmWindow(self):
        self.my_alarm = PresentationLayer.Alarm.AlarmWindow()


class OptionScreenController():
    def __init__(self, option_window):
        self.my_option = option_window




