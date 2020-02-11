import re
import os
import gi
gi.require_version('Gtk', '3.0')

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO library!")
    print("It is correct if it isn't run on a Raspberry pi.")
    print("If is run on Raspberry, try to run 'sudo python Principal.py'")
    print("This program need superuser privileges to manage GPIO.")
    print("RPi.GPIO library can controls the power to the speakers. If you needn't this feature, don't worry.")

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