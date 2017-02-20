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
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyAlarmEvent.SOUND_ALARM, self.sound_alarm)
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

        self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyInfoEvent.SET_NEW_MESSAGE, self.set_info_message
            )
        self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyInfoEvent.DELETE_MESSAGE, self.delete_info_message
            )
        self.logic_controller.get_display_messages()
        start_gui()

    def set_info_message(self, event):
        self.window.add_msg(event.data[0], event.data[1])

    def delete_info_message(self, event):
        self.window.delete_message(event.data[0])

    def get_library_items(self):
        library = self.logic_controller.get_library_list()
        self.window.reload_library_items(library)

    def open_library_manager(self):
        if self.my_library is None:
            self.my_library = LibraryScreenController(event_dispatcher=self.event_dispatcher,
                                                      logic_controller=self.logic_controller)
        self.my_library.show_window()

    def open_alarm_manager(self):
        if self.my_alarm is None:
            self.my_alarm = AlarmScreenController(event_dispatcher=self.event_dispatcher,
                                                  logic_controller=self.logic_controller)
        self.my_alarm.show_window()

    def sound_alarm(self, event):
        if self.my_alarm is None:
            self.my_alarm = AlarmScreenController(event_dispatcher=self.event_dispatcher,
                                                  logic_controller=self.logic_controller)
        self.my_alarm.sound_alarm(event.data)

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


class LibraryScreenController:
    def __init__(self, event_dispatcher=None, logic_controller=None):
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyLibraryEvent.SET_LIBRARY_LIST, self.reload_library_items)
        if logic_controller is None:
            raise Exception('Logic controller is needed')
        else:
            self.logic_controller = logic_controller

    def show_window(self):
        self.window = PresentationLayer.Library.LibraryManagerWindow(self)
        self.get_items()
        self.window.show_all()

    def get_items(self):
        self.library = self.logic_controller.get_library_list()
        self.window.reload_library_items(self.library)

    def reload_library_items(self, event):
        self.window.reload_library_items(event.data)

    def reload_libraries(self):
        self.logic_controller.reload_libraries()

    def save_library(self, library):
        self.logic_controller.save_library(library)

    def play_this_song(self, filename):
        self.logic_controller.play_this_song(filename)

    def stop_song(self):
        self.event_dispatcher.dispatch_event(
            EventDispatcher.EventDispatcher.MyMusicEvent(
                EventDispatcher.EventDispatcher.MyMusicEvent.STOP_MUSIC,
            )
        )

    def open_library_config(self, title=None):
        library = []
        if not title:
            title = "Nueva Biblioteca"
            self.my_new_library_window = PresentationLayer.Library.LibraryConfigWindow(title, self)
        else:
            library_dict = self.logic_controller.get_library_parameters(title)
            library = library_dict['songs']
            title = "Modificar Biblioteca"
            self.my_new_library_window = PresentationLayer.Library.LibraryConfigWindow(title, self)
            self.my_new_library_window.set_library(library)
            self.my_new_library_window.set_library_name(library_dict['name'])

    def delete_library(self, name):
        self.logic_controller.delete_library(name)

    def delete_song_from_library(self, library, song):
        self.logic_controller.delete_song_from_library(library, song)


class AlarmScreenController:
    def __init__(self, event_dispatcher=None, logic_controller=None):
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyAlarmEvent.SET_ALARM_LIST, self.reload_alarm_items)
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyLibraryEvent.SET_LIBRARY_LIST, self.reload_library_items)
        if logic_controller is None:
            raise Exception('Logic controller is needed')
        else:
            self.logic_controller = logic_controller
        self.my_sound_alarm = None

    def show_window(self):
        self.window = PresentationLayer.Alarm.AlarmManager(self)
        self.get_items()
        self.window.show_all()

    def get_items(self):
        self.library = self.logic_controller.get_library_list()
        self.alarm_list = self.logic_controller.get_alarm_list()
        self.window.reload_library_items(self.library)
        self.window.reload_alarm_items(self.alarm_list)

    def save_alarm(self, alarm):
        self.logic_controller.save_alarm(alarm)

    def reload_alarm_items(self, event):
        self.window.reload_alarm_items(event.data)

    def reload_library_items(self, event):
        self.window.reload_library_items(event.data)

    def open_alarm_config(self):
        self.my_alarm = PresentationLayer.Alarm.AlarmConfig(self)
        self.my_alarm.reload_library_items(self.library)

    def modify_alarm_config(self, alarm_name):
        self.my_alarm = PresentationLayer.Alarm.AlarmConfig(self)
        self.my_alarm.reload_library_items(self.library)
        self.my_alarm.load_params(self.logic_controller.get_alarm_parameters(alarm_name))

    def sound_alarm(self, alarm):
        if not self.my_sound_alarm:
            self.my_sound_alarm = PresentationLayer.Alarm.SoundAlarm(self, alarm, self.event_dispatcher)
        else:
            self.my_sound_alarm.add_new_alarm(alarm)

    def delete_my_sound_alarm(self):
        self.my_sound_alarm = None

    def deactivate_alarm(self, alarm_name):
        self.logic_controller.deactivate_alarm(alarm_name)

    def snooze_alarm(self, alarm_name):
        self.logic_controller.snooze_alarm(alarm_name)

    def get_next_alarm_name(self):
        return self.logic_controller.get_next_alarm_name()

    def delete_alarm(self, name):
        self.logic_controller.delete_alarm(name)

    def quick_alarm(self, library, time):
        self.logic_controller.quick_alarm(library, time)

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


class OptionScreenController():
    def __init__(self, event_dispatcher=None):
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher

    def show_all(self):
        self.window = PresentationLayer.Option.OptionWindow(my_option_screen_controller=self)
        self.window.show_all()


