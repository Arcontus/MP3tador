#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import PresentationLayer.Main
import PresentationLayer.Library
import PresentationLayer.Alarm
import PresentationLayer.Option

def initializing():
    win = PresentationLayer.Main.MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    return True

class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class MainScreenController(Borg):
    def __init__(self, main_window=None):
        Borg.__init__(self)
        if (main_window != None):
            self.window = main_window

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
    def __init__(self, alarm_window):
        self.window = alarm_window

    def openAlarmWindow(self):
        self.my_alarm = PresentationLayer.Alarm.AlarmWindow()

class OptionScreenController():
    def __init__(self, option_window):
        self.my_option = option_window




