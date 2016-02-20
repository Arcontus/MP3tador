import os.path
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject, GdkPixbuf

power_speakers = False
power_speakers_GPIO = 0

class Opciones(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Opciones")
        self.window = Gtk.Table(1, 1, True)
        self.set_border_width(20)
        self.add(self.window)

        self.sw_power_speakers= Gtk.Switch()
        self.lbl_power_speakers = Gtk.Label(label="Power Speakers")
        self.sw_power_speakers.connect("notify::active", self.on_sw_power_speakers)

        self.lst_GPIO_pinout = Gtk.ComboBoxText()
        self.add_GPIO_pinout()
        self.lst_GPIO_pinout.connect("changed", self.on_lst_GPIO_pinout)
        self.lst_GPIO_pinout.set_active(2)

        self.window.attach(self.lbl_power_speakers, 0,2, 0,1)
        self.window.attach(self.sw_power_speakers, 3,4, 0,1)
        self.window.attach(self.lst_GPIO_pinout, 5,6, 0,1)

        self.show_all()

    def add_GPIO_pinout(self):
        ##### List of all available GPIO on Raspberry py 2 with integrated touch screen #####
        self.lst_GPIO_pinout.append_text("GPIO 5")
        self.lst_GPIO_pinout.append_text("GPIO 6")
        self.lst_GPIO_pinout.append_text("GPIO 12")
        self.lst_GPIO_pinout.append_text("GPIO 13")
        self.lst_GPIO_pinout.append_text("GPIO 16")
        self.lst_GPIO_pinout.append_text("GPIO 19")
        self.lst_GPIO_pinout.append_text("GPIO 20")
        self.lst_GPIO_pinout.append_text("GPIO 21")
        self.lst_GPIO_pinout.append_text("GPIO 26")

    def on_lst_GPIO_pinout(self, widget):
        self.on_sw_power_speakers(widget, widget)


    def on_sw_power_speakers(self, widget, gparam):
        Opciones.power_speakers = self.sw_power_speakers.get_active()
        if (Opciones.power_speakers == True):
            power_speakers_GPIO = self.lst_GPIO_pinout.get_active_text()[5:]
            print(power_speakers_GPIO)



