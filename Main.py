#!/usr/bin/env python
# -*- coding: utf-8 -*-


import LogicLayer.LogicController
import PresentationLayer.PresentationController
import EventDispatcher.EventDispatcher

dispatcher = EventDispatcher.EventDispatcher.EventDispatcher()
main = LogicLayer.LogicController.MainLogicController(event_dispatcher=dispatcher)
main_screen = PresentationLayer.PresentationController.MainScreenController(event_dispatcher=dispatcher)
start = PresentationLayer.PresentationController.start_gui()





