import re
import gi

gi.require_version('Gtk', '3.0')

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO library!")
    print("It is correct if it isn't run on a Raspberry pi.")
    print("If is run on Raspberry, try to run 'sudo python Main.py'")
    print("This program need superuser privileges to manage GPIO.")
    print("RPi.GPIO library can controls the power to the speakers. If you needn't this feature, don't worry.")


class GPIOController:
    GPIO_num = 12
    platform = None

    def __init__(self):
        # make it private
        self.platform = self.platform_detect()

    def platform_detect(self):
        """Detect if running on the Raspberry Pi and return the platform type.
        Will return RASPBERRY_PI, or OTHER."""
        # Handle Raspberry Pi
        pi = self.pi_version()
        if pi is not None:
            return "RASPBERRY_PI " + str(pi)
        else:
            return "OTHER"

    @staticmethod
    def pi_version():
        """Detect the version of the Raspberry Pi.  Returns either 1, 2 or
        None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
        Raspberry Pi 2 (model B+), or not a Raspberry Pi.
        """
        # Check /proc/cpuinfo for the Hardware field value.
        # 2708 is pi 1
        # 2709 is pi 2
        # 2711 is pi
        # 2835 is pi
        # 2836 is pi
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
        elif match.group(1) == 'BCM2711':
            # Pi 4
            return 4
        elif match.group(1) == 'BCM2835':
            # Pi 1
            return 1
        elif match.group(1) == 'BCM2836':
            # Pi 2B
            return 1
        elif match.group(1) == 'BCM2837':
            # Pi 2B
            return 1
        else:
            # Something else, not a pi.
            return None

    ## Power on speakers with GPIO Relay
    def encender_altavoces(self):
        print("Encendiendo altavoces")
        if self.platform != "OTHER":
            # The script as below using BCM GPIO 00..nn numbers
            GPIO.setmode(GPIO.BCM)
            # Set relay pins as output
            GPIO.setup(self.GPIO_num, GPIO.OUT)
            GPIO.output(self.GPIO_num, True)

    ## Power down speakers with GPIO Relay
    def apagar_altavoces(self):
        print("Apagando altavoces")
        if self.platform != "OTHER":
            # The script as below using BCM GPIO 00..nn numbers
            GPIO.setmode(GPIO.BCM)
            # Set relay pins as output
            GPIO.setup(self.GPIO_num, GPIO.OUT)
            GPIO.output(self.GPIO_num, False)

