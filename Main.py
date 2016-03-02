#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PresentationLayer.Main import Main

win = Main()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()