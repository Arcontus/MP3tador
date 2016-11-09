"""
Module to control all things about the presentation layer:
* Manage screens.
* Open new screens.
* Comuniation with logic controller.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "David Pozos Ceron"

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import PresentationLayer.Main
import PresentationLayer.Library
import PresentationLayer.Alarm
import PresentationLayer.Option
import EventDispatcher.EventDispatcher




def start_gui():
    Gtk.main()


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class MainScreenController(Borg):
    def __init__(self, main_window=None, event_dispatcher=None, logic_controller=None):
        Borg.__init__(self)
        if main_window is not None:
            self.window = main_window
        else:
            self.window = PresentationLayer.Main.MainWindow(self)
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_HOUR, self.set_hour)
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_DATE, self.set_date)
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyLibraryEvent.SET_LIBRARY_LIST, self.reload_library_items)
        if logic_controller is None:
            raise NameError('Logic controller is needed')
        else:
            self.logic_controller = logic_controller

        self.my_alarm = None
        self.my_library = None
        self.my_option = None
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()
        self.get_library_items()
        start_gui()

    def get_library_items(self):
        library = self.logic_controller.get_library_list()
        self.window.reload_library_items(library)

    def open_library_manager(self):
        self.my_library = PresentationLayer.Library.LibraryManagerWindow()
        self.my_library.show_all()

    def open_alarm_manager(self):
        if self.my_alarm is None:
            self.my_alarm = AlarmScreenController(event_dispatcher=self.event_dispatcher, logic_controller=self.logic_controller )
        self.my_alarm.show_window()

    def open_option_manager(self):
        if self.my_option is None:
            self.my_option = OptionScreenController(event_dispatcher=self.event_dispatcher)
        self.my_option.show_all()

    def set_hour(self, hour):
        self.window.set_hour(hour)

    def set_date(self, date):
        self.window.set_date(date)

    def reload_library_items(self, event):
        self.window.reload_library_items(event.data)

    def set_library_player(self, library):
        self.event_dispatcher.dispatch_event(
            EventDispatcher.EventDispatcher.MyMusicEvent(
                EventDispatcher.EventDispatcher.MyMusicEvent.SET_LIBRARY,
                library)
        )

    def play_song(self):
        self.event_dispatcher.dispatch_event(
            EventDispatcher.EventDispatcher.MyMusicEvent(
                EventDispatcher.EventDispatcher.MyMusicEvent.PLAY_MUSIC,
            )
        )

    def stop_song(self):
        self.event_dispatcher.dispatch_event(
            EventDispatcher.EventDispatcher.MyMusicEvent(
                EventDispatcher.EventDispatcher.MyMusicEvent.STOP_MUSIC,
            )
        )

    def pause_song(self):
        self.event_dispatcher.dispatch_event(
            EventDispatcher.EventDispatcher.MyMusicEvent(
                EventDispatcher.EventDispatcher.MyMusicEvent.PAUSE_MUSIC,
            )
        )

    def next_song(self):
        self.event_dispatcher.dispatch_event(
            EventDispatcher.EventDispatcher.MyMusicEvent(
                EventDispatcher.EventDispatcher.MyMusicEvent.NEXT_SONG,
            )
        )


class AlarmScreenController:
    def __init__(self, event_dispatcher=None, logic_controller=None):
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyAlarmEvent.SET_ALARM_LIST, self.reload_alarm_items)
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyLibraryEvent.SET_LIBRARY_LIST, self.reload_library_items)
        if logic_controller is None:
            raise NameError('Logic controller is needed')
        else:
            self.logic_controller = logic_controller

    def show_window(self):
        self.window = PresentationLayer.Alarm.AlarmManager(my_alarm_screen_controller=self)
        self.get_items()
        self.window.show_all()

    def get_items(self):
        library = self.logic_controller.get_library_list()
        self.window.reload_library_items(library)
        alarm = self.logic_controller.get_alarm_list()
        self.window.reload_alarm_items(alarm)

    def reload_alarm_items(self, event):
        self.window.reload_alarm_items(event.data)

    def reload_library_items(self, event):
        self.window.reload_library_items(event.data)

    def open_alarm_window(self):
        self.my_alarm = PresentationLayer.Alarm.AlarmWindow(self)

    def get_next_alarm_name(self):
        return self.logic_controller.get_next_alarm_name()


class OptionScreenController():
    def __init__(self, event_dispatcher=None):
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher

    def show_all(self):
        self.window = PresentationLayer.Option.OptionWindow(my_option_screen_controller=self)
        self.window.show_all()






