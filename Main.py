"""
MP3 Alarm with some advanced options
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = "David Pozos Ceron"

import LogicLayer.LogicController
import PresentationLayer.PresentationController
import EventDispatcher.EventDispatcher
import PresentationLayer.Alarm

dispatcher = EventDispatcher.EventDispatcher.EventDispatcher()
main_logic = LogicLayer.LogicController.MainLogicController(event_dispatcher=dispatcher)
alarm = {'name': '', 'active': False, 'days': False, 'monday': False, 'tuesday': False,
                      'wednesday': False, 'thursday': False, 'friday': False, 'saturday': False, 'sunday': False,
                      'hours': 0, 'minutes': 0, 'library': "Anna", 'snooze': False, 'min_snooze': 5}
#bla = PresentationLayer.Alarm.sound_alarm(alarm)
main_screen = PresentationLayer.PresentationController.MainScreenController(event_dispatcher=dispatcher,
                                                                            logic_controller=main_logic)






