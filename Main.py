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

dispatcher = EventDispatcher.EventDispatcher.EventDispatcher()
main_logic = LogicLayer.LogicController.MainLogicController(event_dispatcher=dispatcher)
main_screen = PresentationLayer.PresentationController.MainScreenController(event_dispatcher=dispatcher,
                                                                            logic_controller=main_logic)






