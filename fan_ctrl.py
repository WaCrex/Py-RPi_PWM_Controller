#!/usr/bin/python3
import RPi.GPIO as GPIO
import json
from time import sleep

# Load User settings
with open(__file__.replace('.py','.json')) as file:
    config = json.load(file)
    
# Load Fan Profile
curve = config['profiles'][config['profile']]

# Use Broadcom GPIO Numbers
GPIO.setmode(GPIO.BCM)

# Initialize GPIO Pin
GPIO.setup(config['gpio_pin'], GPIO.OUT)

# Set PWM Frequency
fan = GPIO.PWM(config['gpio_pin'], config['pwm_freq'])

# PWM Start with fan turned off
fan.start(0)

# User Settings no longer needed
config.clear()

# The current CPU Fan status (on/off)
status = False

# Temp history, used for calculating trend
history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# noinspection PyBroadException
try:
    # The main loop
    while True:
        # Get CPU Temp
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as sensor:
            temp = int(float(sensor.read()) / 1000)
        
        # Reset the fan speed
        speed = 0

        # Should the fan be turned off?
        if temp <= 40:
            # Turn off the fan
            status = False

        # Is the fan on or should it be?
        elif status or temp >= 50:
            # Clamp the temperature to the fan curve
            if temp <= 50:
                index = 0
            elif temp > 80:
                index = 30
            else:
                index = temp - 50
            
            # Check if it's an upward trend
            if ((sum(history) / 10) < temp) or temp < 50:
                # Try to stabilize the temperature
                # TODO: Need to test this further
                if index < 30:
                    index += 1
                
            # Remove the first entry
            history.pop(0)
            
            # Add temperature to the list
            history.append(temp)
            
            # Load fan speed from curve
            speed = curve[index]
            
            # Keep the fan on
            status = True
        
        # Update fan speed
        fan.ChangeDutyCycle(speed)

        # Go back to sleep... ZzZzZz
        sleep(2.00)

# Did the code crash?
# TODO: Check if this is safe enough, or if further steps should be taken.
except Exception as _e:
    # Set the CPU Fan speed to 100%
    fan.ChangeDutyCycle(100)

