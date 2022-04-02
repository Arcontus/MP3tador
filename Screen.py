import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from subprocess import run

def button_callback(channel):
    global screen_state
    if screen_state:
        run('vcgencmd display_power 0', 'shel=True') #Turn off the display
        screen_state = False
    else:
        run('vcgencmd display_power 1', 'shel=True')  # Turn on the display
        screen_state = True


screen_state = True

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 20 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(16,GPIO.RISING,callback=button_callback) # Setup event on pin 20 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up