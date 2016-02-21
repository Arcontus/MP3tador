import os.path
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")
    print("This is probably because you need superuser privileges.")
    print("You can achieve this by using 'sudo' to run your script")

from time import sleep

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject, GdkPixbuf

power_speakers = 0
power_speakers_GPIO = 12

def cargar_parametros():
    global power_speakers
    global power_speakers_GPIO
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



class MenuOpciones(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Opciones")
        self.window = Gtk.Table(1, 1, True)
        self.set_border_width(20)
        self.add(self.window)

        ##### List of all available GPIO on Raspberry py 2 with integrated touch screen #####
        self.GPIO_pinout_list = ["GPIO 5", "GPIO 6", "GPIO 12", "GPIO 13", "GPIO 16", "GPIO 19", "GPIO 20", "GPIO 21", "GPIO 26"]

        self.lst_GPIO_pinout = Gtk.ComboBoxText()
        self.add_GPIO_pinout()
        self.lst_GPIO_pinout.set_active(2)
        self.lst_GPIO_pinout.connect("changed", self.on_lst_GPIO_pinout)

        self.sw_power_speakers= Gtk.Switch()
        self.lbl_power_speakers = Gtk.Label(label="Encender Altavoces")
        self.sw_power_speakers.connect("notify::active", self.on_sw_power_speakers)

        self.load_options()

        self.btn_guardar = Gtk.Button(label="Guardar")
        self.btn_guardar.connect("clicked", self.on_btn_guardar_clicked)


        self.window.attach(self.lbl_power_speakers, 0,2, 0,1)
        self.window.attach(self.sw_power_speakers, 3,4, 0,1)
        self.window.attach(self.lst_GPIO_pinout, 5,6, 0,1)
        self.window.attach(self.btn_guardar, 1,2, 2,3)


        self.show_all()

    def on_btn_guardar_clicked(self, widget):
        self.save_options()

    def load_options(self):
        global power_speakers
        global power_speakers_GPIO
        if (os.path.isfile("opciones.txt") == True):
            fichero = open("opciones.txt", "r")
            for line in fichero:
                if (line.split(":")[0] == 'power_speakers'):
                    if ((line.split(":")[1]) == "True\n"):
                        power_speakers = True
                    else:
                        power_speakers = False
                    self.sw_power_speakers.set_active(power_speakers)

                elif (line.split(":")[0] == "power_speakers_GPIO"):
                    power_speakers_GPIO = int(line.split(":")[1])
                    self.lst_GPIO_pinout.set_active(self.get_GPIO_pinout_lst_position_by_num(power_speakers_GPIO))

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







