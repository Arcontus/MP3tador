"""
Manage all functions of the logic program and take decisions and events about it:
* Implements all public functions for the presentation layer.
* All notifications with presentation layer is used with events.
* The communication with DataController is direct, its means that DataController exposes functions
that is used only by LogicController.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "David Pozos Ceron"

import re
import DataLayer.DataController
import LogicLayer.Clock
import LogicLayer.MusicPlayer
import EventDispatcher.EventDispatcher
from gi.repository import GObject


class MainLogicController:
    def __init__(self, event_dispatcher=None):
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyMusicEvent.SET_LIBRARY, self.set_player_library)
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyMusicEvent.PLAY_MUSIC, self.play_song)
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyMusicEvent.STOP_MUSIC, self.stop_song)
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyMusicEvent.NEXT_SONG, self.next_song)
            self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyMusicEvent.PAUSE_MUSIC, self.pause_song)
        self.data = DataLayer.DataController.MainDataController(event_dispatcher=self.event_dispatcher)
        self.clock = LogicLayer.Clock.Clock()
        self.alarm = LogicLayer.Clock.Alarm(self, self.clock)
        self.player = LogicLayer.MusicPlayer.MusicPlayer(self, event_dispatcher)
        self.last_minute_check = -1
        self._update_id = GObject.timeout_add(1000, self.update_time, None)


    def update_time(self, extra):
        # Here the code to check every second
        # Event for update hour
        self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyDateEvent(
                        EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_HOUR,
                        self.clock.get_time_formated()
                )
        )

        current_minute = self.clock.get_minutes()
        if self.last_minute_check is not current_minute:
            self.last_minute_check = current_minute
            # Here the code to check every minute
            self.alarm.check_alarms()
            self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyDateEvent(
                        EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_DATE,
                        self.clock.get_date_formated()
                )
            )
        return True

    def get_alarm_list(self):
        my_list = self.data.get_alarm_list()
        list_names = []
        for i in my_list:
            list_names.append(i.get_name())
        return list_names

    def get_library_list(self):
        my_list = self.data.get_library_list()
        list_names = []
        for i in my_list:
            list_names.append(i.get_name())
        return list_names

    # This method read the list of alarm names, and compare with his pattern.
    # If the pattern exists, it try with patern(n) where (n) is the next free number.
    def get_next_alarm_name(self):
        pattern = "Alarm"
        number = 1
        next_name = None
        my_alarm_list = self.get_alarm_list()
        while next_name is None:
            name = pattern + str(number)
            if name in my_alarm_list:
                number += 1
            else:
                next_name = name
        return next_name

    def set_player_library(self, event):
        if event.data is not None:
            if self.validate_filename(event.data):
                self.player.load_library(event.data)
        else:
            self.player.unload_library()

    def save_alarm(self, dict):
        if self.validate_filename(dict['name']):
            if self.data.save_alarm(dict):
                self.event_dispatcher.dispatch_event(
                    EventDispatcher.EventDispatcher.MyAlarmEvent(
                            EventDispatcher.EventDispatcher.MyAlarmEvent.SET_ALARM_LIST,
                            self.get_alarm_list()
                    )
                )

    def delete_alarm(self, name):
        if self.data.delete_alarm(name):
            self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyAlarmEvent(
                        EventDispatcher.EventDispatcher.MyAlarmEvent.SET_ALARM_LIST,
                        self.get_alarm_list()
                )
            )

    def save_library(self, dict):
        if self.validate_filename(dict['name']):
            if self.data.save_library(dict):
                self.event_dispatcher.dispatch_event(
                    EventDispatcher.EventDispatcher.MyLibraryEvent(
                            EventDispatcher.EventDispatcher.MyLibraryEvent.SET_LIBRARY_LIST,
                            self.get_library_list()
                    )
                )

    def reload_libraries(self):
        self.event_dispatcher.dispatch_event(
            EventDispatcher.EventDispatcher.MyLibraryEvent(
                    EventDispatcher.EventDispatcher.MyLibraryEvent.SET_LIBRARY_LIST,
                    self.get_library_list()
            )
        )

    def delete_library(self, name):
        if self.data.delete_library(name):
            self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyLibraryEvent(
                    EventDispatcher.EventDispatcher.MyLibraryEvent.SET_LIBRARY_LIST,
                    self.get_library_list()
                )
            )

    def delete_song_from_library(self, library, song):
        if self.data.delete_song_from_library(library, song):
            self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyLibraryEvent(
                    EventDispatcher.EventDispatcher.MyLibraryEvent.SET_LIBRARY_LIST,
                    self.get_library_list()
                )
            )

    def get_alarm_parameters(self, name):
        return self.data.get_alarm_parameters(name)

    def get_library_parameters(self, name):
        return self.data.get_library_parameters(name)

    def play_song(self, event):
        self.player.play()

    def play_this_song(self, filename):
        self.player.play_this_song(filename)

    def stop_song(self, event):
        self.player.stop()

    def pause_song(self, event):
        self.player.pause()

    def next_song(self, event):
        self.player.play_next_song()

    @staticmethod
    def validate_filename(filename):
        if filename:
            if re.match(r'[A-Za-z0-9_\-\\]', filename):
                return True
        return False








