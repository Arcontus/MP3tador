#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MP3 Alarm with some advanced options
"""
__author__ = "David Pozos Cerón"

import LogicLayer.LogicController
import PresentationLayer.PresentationController
import EventDispatcher.EventDispatcher

dispatcher = EventDispatcher.EventDispatcher.EventDispatcher()
main_logic = LogicLayer.LogicController.MainLogicController(event_dispatcher=dispatcher)
main_screen = PresentationLayer.PresentationController.MainScreenController(event_dispatcher=dispatcher,
                                                                            logic_controller=main_logic)






