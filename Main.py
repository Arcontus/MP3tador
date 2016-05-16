#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PresentationLayer.PresentationController import initializing
import LogicLayer.LogicController
import EventDispatcher.EventDispatcher

dispatcher = EventDispatcher.EventDispatcher.EventDispatcher()
main = LogicLayer.LogicController.MainLogicController(dispatcher)



