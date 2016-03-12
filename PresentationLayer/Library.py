# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class LibraryManagerWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Biblioteca")
        window = Gtk.Table(1, 1, True)
        self.set_border_width(20)
        self.add(window)
        self.connect('delete-event', self.delete_event)
        self.lst_library = Gtk.ComboBoxText()

        self.btn_add_library = Gtk.Button(label="Nueva biblioteca")
        self.btn_add_library.connect("clicked", self.on_btn_add_library_clicked)

        self.btn_rm_library = Gtk.Button(label="Eliminar")
        self.btn_rm_library.connect("clicked", self.on_btn_rm_library_clicked)

        self.btn_mdf_library = Gtk.Button(label="Modificar")
        self.btn_mdf_library.connect("clicked", self.on_btn_mdf_library_clicked)

        window.attach(self.btn_add_library, 2,5,0,1)
        window.attach(self.lst_library, 2, 5, 2, 3)
        window.attach(self.btn_rm_library, 0,1,2,3)
        window.attach(self.btn_mdf_library, 6,7 ,2,3)

    def reload_items(self, widget1, widget2):
        a =1

    def reload_list(self):
        a =1

    def add_item(self, item):
        a =1

    def on_btn_add_library_clicked(self, widget):
        a =1

    def get_library(self):
        a =1

    def on_btn_rm_library_clicked(self, widget):
        a =1

    def on_btn_mdf_library_clicked(self, widget):
        a =1

    def error_rm_params(self, num):
        a =1

    def delete_event(self, widget, event=None):
        a =1