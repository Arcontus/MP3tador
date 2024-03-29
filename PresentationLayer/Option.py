# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import PresentationLayer.PresentationController

class OptionWindow(Gtk.Window):
    def __init__(self, my_option_screen_controller=None):
        if my_option_screen_controller:
            self.my_option_screen_controller = my_option_screen_controller
        else:
            raise NameError("OptionWindow needs option_screen_controller instance")

        self.options = {'GPIO': 12, 'is_enable_GPIO': False}

        Gtk.Window.__init__(self, title="Options")
        self.window = Gtk.Table(1, 1, True)
        self.set_border_width(20)
        self.add(self.window)

        # List of all available GPIO on Raspberry py 2 with integrated touch screen #####
        # If you need any other GPIO ID, please, add in the next list.
        self.GPIO_pinout_list = ["GPIO 5", "GPIO 6", "GPIO 12", "GPIO 13", "GPIO 16", "GPIO 19", "GPIO 20", "GPIO 21", "GPIO 26"]

        self.lst_GPIO_pinout = Gtk.ComboBoxText()
        self.add_GPIO_pinout()
        self.lst_GPIO_pinout.set_active(2)
        self.lst_GPIO_pinout.connect("changed", self.on_lst_GPIO_pinout)

        self.sw_power_speakers = Gtk.Switch()
        self.lbl_power_speakers = Gtk.Label(label="Switch On Speakers (Only for Raspberry)")
        self.sw_power_speakers.connect("notify::active", self.on_sw_power_speakers)

        self.lbl_auto_stop_alarm = Gtk.Label(label="Switch off alarm after")
        adj_hours = Gtk.Adjustment(0, 10, 240, 15, 0, 0)
        self.spb_hours = Gtk.SpinButton()
        self.spb_hours.set_adjustment(adj_hours)
        self.spb_hours.connect("value_changed", self.on_spb_hours_change)
        self.lbl_auto_stop_alarm_hours = Gtk.Label(label="hours")

        self.btn_guardar = Gtk.Button(label="Save")
        self.btn_guardar.connect("clicked", self.on_btn_guardar_clicked)

        self.window.attach(self.lbl_power_speakers, 0,3, 0,1)
        self.window.attach(self.sw_power_speakers, 3,4, 0,1)
        self.window.attach(self.lbl_auto_stop_alarm, 1,3 ,1,2)
        self.window.attach(self.spb_hours,3,4, 1,2)
        self.window.attach(self.lbl_auto_stop_alarm_hours, 4,5, 1,2)
        self.window.attach(self.lst_GPIO_pinout, 4, 5, 0,1)
        self.window.attach(self.btn_guardar, 1,2, 2,3)
        self.show_all()

    def on_btn_guardar_clicked(self, widget):
        self.my_option_screen_controller.save_options(self.options)

    def load_options(self, option_dic):
        self.options = option_dic
        self.sw_power_speakers.set_active(self.options["is_enable_GPIO"])
        self.lst_GPIO_pinout.set_active(self.get_GPIO_pinout_lst_position_by_num(self.options["GPIO"]))
        self.spb_hours.set_text(str(self.options["auto_stop_after_minutes"]))
        self.update_sensitives()

    def add_GPIO_pinout(self):
        for i in self.GPIO_pinout_list:
            self.lst_GPIO_pinout.append_text(i)

    def get_GPIO_pinout_lst_position_by_num(self, num):
        posicion = 0
        for i in self.GPIO_pinout_list:
            if (int(i[5:]) == int(num)):
                return posicion
            posicion = posicion + 1
        return False

    def on_lst_GPIO_pinout(self, widget):
        self.options["GPIO"] = self.lst_GPIO_pinout.get_active_text()[5:]
        self.update_sensitives()
        self.on_sw_power_speakers(widget, widget)

    def on_sw_power_speakers(self, widget, gparam):
        self.options["is_enable_GPIO"] = self.sw_power_speakers.get_active()
        self.update_sensitives()
        #     self.get_GPIO_pinout_lst_position_by_num(self.options["GPIO"])

    def update_sensitives(self):
        # Comprobamos el status del switch GPIO
        self.lst_GPIO_pinout.set_sensitive(self.options["is_enable_GPIO"])

    def on_spb_hours_change(self, val1=None, val2=None):
        self.options["auto_stop_after_minutes"] = self.spb_hours.get_text()
