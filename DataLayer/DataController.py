"""
Manage all things about the data and files and exposes some public functions for using on
LogicController.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "David Pozos Ceron"

import DataLayer.Library
import DataLayer.Alarm
import DataLayer.Options


class MainDataController:
    def __init__(self, event_dispatcher=None):
        if event_dispatcher is not None:
            self.event_dispatcher = event_dispatcher
        DataLayer.Library.load_library_list()
        DataLayer.Alarm.load_alarm_list()
        DataLayer.Options.load_options()

    @staticmethod
    def get_alarm_list():
        return DataLayer.Alarm.get_alarm_list()

    @staticmethod
    def get_library_list():
        return DataLayer.Library.get_library_list()

    @staticmethod
    def get_options():
        return DataLayer.Options.get_options()

    @staticmethod
    def get_alarm(name):
        if name is None:
            return None
        else:
            return DataLayer.Alarm.get_alarm_by_name(name)

    @staticmethod
    def get_library(name):
        if name is None:
            return None
        else:
            return DataLayer.Library.get_library_by_name(name)

    @staticmethod
    def get_alarm_parameters(name):
        my_alarm = DataLayer.Alarm.get_alarm_by_name(name)
        if my_alarm:
            alarm_dic = {'name': my_alarm.get_name(), 'active': my_alarm.get_active(), 'days': my_alarm.get_days(),
                         'monday': my_alarm.get_monday(), 'tuesday': my_alarm.get_tuesday(),
                         'wednesday': my_alarm.get_wednesday(), 'thursday': my_alarm.get_thursday(),
                         'friday': my_alarm.get_friday(), 'saturday': my_alarm.get_saturday(),
                         'sunday': my_alarm.get_sunday(), 'hours': my_alarm.get_hours(), 'minutes': my_alarm.get_minutes(),
                         'library': my_alarm.get_library(), 'snooze': my_alarm.get_snooze(),
                         'min_snooze': my_alarm.get_min_snooze()}
            return alarm_dic
        return False  # Not found

    @staticmethod
    def get_library_parameters(name):
        my_library = DataLayer.Library.get_library_by_name(name)
        if my_library:
            library_dic = {'name': my_library.get_name(), 'items': my_library.get_num_items(),
                           'songs': my_library.get_songs()}
            print(library_dic)
            return library_dic
        return False  # Not found

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

    @staticmethod
    def save_library(library_dict):
        add_library = False
        my_library = DataLayer.Library.get_library_by_name(library_dict['name'])
        if not my_library:
            print("library not found")
            my_library = DataLayer.Library.Library()
            add_library = True
        my_library.remove_all_songs()
        my_library.set_name(library_dict['name'])
        my_library.add_song_list(library_dict['songs'])
        my_library.save_params()
        if add_library:
            DataLayer.Library.add_library(my_library)
            return True
        else:
            return False

    @staticmethod
    def save_options(options_dict):
        my_options = DataLayer.Options.Options()
        my_options.set_is_enable_GPIO(options_dict['is_enable_GPIO'])
        my_options.set_GPIO(options_dict['GPIO'])
        my_options.set_is_enable_auto_stop(options_dict['is_enable_auto_stop'])
        my_options.set_auto_stop_after_minutes(options_dict['auto_stop_after_minutes'])
        my_options.save_params()

    @staticmethod
    def delete_alarm(name):
        if DataLayer.Alarm.rm_alarm_by_name(name):
            print ("alarm '{}' deleted.".format(name))
            return True
        return False

    @staticmethod
    def delete_library(name):
        if DataLayer.Library.rm_library_by_name(name):
            print ("library '{}' deleted.".format(name))
            return True
        return False

    @staticmethod
    def delete_song_from_library(library, song):
        my_library = DataLayer.Library.get_library_by_name(library)
        if my_library:
            return my_library.del_song(song)
        return False

