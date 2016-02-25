###


import os.path
import platform
import re


try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")
    print("It is correct if it isn't run on a Raspberry pi.")
    print("If is run on Raspberry, try to run 'sudo python Principal.py'")
    print("This program need superuser privileges to manage GPIO.")

from time import sleep

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject, GdkPixbuf

power_speakers = 0
power_speakers_GPIO = 12
my_platform = None

def platform_detect():
    """Detect if running on the Raspberry Pi and return the platform type.
    Will return RASPBERRY_PI, or OTHER."""
    # Handle Raspberry Pi
    pi = pi_version()
    if pi is not None:
        return "RASPBERRY_PI "+str(pi)
    else:
        return "OTHER"

def pi_version():
    """Detect the version of the Raspberry Pi.  Returns either 1, 2 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), or not a Raspberry Pi.
    """
    # Check /proc/cpuinfo for the Hardware field value.
    # 2708 is pi 1
    # 2709 is pi 2
    # Anything else is not a pi.
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
    # Match a line like 'Hardware   : BCM2709'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                      flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Couldn't find the hardware, assume it isn't a pi.
        return None
    if match.group(1) == 'BCM2708':
        # Pi 1
        return 1
    elif match.group(1) == 'BCM2709':
        # Pi 2
        return 2
    else:
        # Something else, not a pi.
        return None

## Load option parameters.
def cargar_parametros():
    global my_platform
    global power_speakers
    global power_speakers_GPIO
    my_platform = platform_detect()
    print(my_platform)
    if (my_platform != "OTHER"):
        if (os.path.isfile("opciones.txt") == True):
            fichero = open("opciones.txt", "r")
            for line in fichero:
                if (line.split(":")[0] == 'power_speakers'):
                    if ((line.split(":")[1]) == "True\n"):
                        power_speakers = True
                    else:
                        power_speakers = False
                elif (line.split(":")[0] == "power_speakers_GPIO"):
                    power_speakers_GPIO = int(line.split(":")[1])
    else:
        power_speakers = False  #Si no se corre en una Raspberry, mantener a False.

## Power on speakers with GPIO Relay
def encender_altavoces():
    global power_speakers
    global power_speakers_GPIO
    if (power_speakers):
        # The script as below using BCM GPIO 00..nn numbers
        GPIO.setmode(GPIO.BCM)
        # Set relay pins as output
        GPIO.setup(power_speakers_GPIO, GPIO.OUT)
        GPIO.output(power_speakers_GPIO, True)
        print("Encendiendo altavoces")

## Power down speakers with GPIO Relay
def apagar_altavoces():
    global power_speakers
    global power_speakers_GPIO
    if (power_speakers):
        # The script as below using BCM GPIO 00..nn numbers
        GPIO.setmode(GPIO.BCM)
        # Set relay pins as output
        GPIO.setup(power_speakers_GPIO, GPIO.OUT)
        GPIO.output(power_speakers_GPIO, False)
        print ("Apagando altavoces")


## Option window menu
class MenuOpciones(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Opciones")
        self.window = Gtk.Table(1, 1, True)
        self.set_border_width(20)
        self.add(self.window)

        ##### List of all available GPIO on Raspberry py 2 with integrated touch screen #####
        ##### If you need any other GPIO ID, please, add in the next list.
        self.GPIO_pinout_list = ["GPIO 5", "GPIO 6", "GPIO 12", "GPIO 13", "GPIO 16", "GPIO 19", "GPIO 20", "GPIO 21", "GPIO 26"]

        self.lst_GPIO_pinout = Gtk.ComboBoxText()
        self.add_GPIO_pinout()
        self.lst_GPIO_pinout.set_active(2)
        self.lst_GPIO_pinout.connect("changed", self.on_lst_GPIO_pinout)

        self.sw_power_speakers= Gtk.Switch()
        self.lbl_power_speakers = Gtk.Label(label="Encender Altavoces (Solo para Raspberry)")
        self.sw_power_speakers.connect("notify::active", self.on_sw_power_speakers)

        self.load_options()

        self.btn_guardar = Gtk.Button(label="Guardar")
        self.btn_guardar.connect("clicked", self.on_btn_guardar_clicked)

        self.window.attach(self.lbl_power_speakers, 0,3, 0,1)
        self.window.attach(self.sw_power_speakers, 3,4, 0,1)
        self.window.attach(self.lst_GPIO_pinout, 4, 5, 0,1)
        self.window.attach(self.btn_guardar, 1,2, 2,3)
        self.show_all()

    def on_btn_guardar_clicked(self, widget):
        self.save_options()

    def load_options(self):
        global power_speakers
        global power_speakers_GPIO
        global my_platform
        if (os.path.isfile("opciones.txt") == True):
            fichero = open("opciones.txt", "r")
            for line in fichero:
                if (my_platform != "OTHER"): ##Block to execute only on Raspberry pi
                    if (line.split(":")[0] == 'power_speakers'):
                        if ((line.split(":")[1]) == "True\n"):
                            power_speakers = True
                        else:
                            power_speakers = False
                        self.sw_power_speakers.set_active(power_speakers)

                    elif (line.split(":")[0] == "power_speakers_GPIO"):
                        power_speakers_GPIO = int(line.split(":")[1])
                        self.lst_GPIO_pinout.set_active(self.get_GPIO_pinout_lst_position_by_num(power_speakers_GPIO))
                else:
                    self.sw_power_speakers.set_sensitive(False)
                    self.lst_GPIO_pinout.set_sensitive(False)

        else :
            power_speakers_GPIO = self.lst_GPIO_pinout.get_active_text()[5:]

    def save_options(self):
        global power_speakers
        global power_speakers_GPIO
        fichero = open("opciones.txt", "w")
        fichero.write("power_speakers:"+str(power_speakers)+"\n")
        fichero.write("power_speakers_GPIO:"+str(power_speakers_GPIO)+"\n")
        fichero.close()

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
        self.on_sw_power_speakers(widget, widget)


    def on_sw_power_speakers(self, widget, gparam):
        global power_speakers
        global power_speakers_GPIO
        power_speakers = self.sw_power_speakers.get_active()
        if (power_speakers == True):
            power_speakers_GPIO = self.lst_GPIO_pinout.get_active_text()[5:]
            self.get_GPIO_pinout_lst_position_by_num(power_speakers_GPIO)







