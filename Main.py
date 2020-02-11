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

# alarm = {'name': 'prueba', 'active': False, 'days': False, 'monday': False, 'tuesday': False,
#                       'wednesday': False, 'thursday': False, 'friday': False, 'saturday': False, 'sunday': False,
#                       'hours': 0, 'minutes': 0, 'library': "Anna", 'snooze': False, 'min_snooze': 5}
# alarm2 = {'name': 'prueba2', 'active': False, 'days': False, 'monday': False, 'tuesday': False,
#                       'wednesday': False, 'thursday': False, 'friday': False, 'saturday': False, 'sunday': False,
#                       'hours': 0, 'minutes': 0, 'library': "Anna", 'snooze': False, 'min_snooze': 5}
#
# alarmsc = PresentationLayer.PresentationController.AlarmScreenController(dispatcher, main_logic)
# alarmsc.sound_alarm(alarm)
# alarmsc.sound_alarm(alarm2)

main_screen = PresentationLayer.PresentationController.MainScreenController(event_dispatcher=dispatcher,
                                                                            logic_controller=main_logic)







