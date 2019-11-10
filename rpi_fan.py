#!/usr/bin/env python
# -*- coding:utf-8 -*

'''
Régulation de la température d'un Raspberry pi avec un ventillateur

Entrée : Température GPU via vcgencmd
Sortie : Ventillateur via transistor NPN

Rpi         NPN              FAN
GPIO18 ---- Base
0V -------- Collecteur
            Emetteur ------- 0V FAN
5V -------------------------- + FAN
'''

#TODO (si necessaire) : faire du PWM pour réguler la vitesse du ventilateur + PID

import sys
import time
from subprocess import PIPE, Popen

try:
    import RPi.GPIO as GPIO
except ImportError:
    sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib') # for LibreELEC distribition
    import RPi.GPIO as GPIO


class Rpi_fan:
    ''' Un régulateur de température
    '''
    def __init__(self, target_temp = 45, pin = 24):
        '''Initialisation :
            target_temp     :   the target temperature °C (default : 45°C)
            pin             :   the GPIO (default : GPIO18)
        '''
        self.target_temp = target_temp
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def run(self, delay = 1):
        '''Run forever
            delay           :   duration (second) between mesures
        '''
        while True:
            temp = self.get_gpu_temperature()
            print("Temperature : %s°C"%temp)
            if temp > self.target_temp:
                GPIO.output(self.pin, GPIO.HIGH)
                print("Fan on")
            else:
                GPIO.output(self.pin, GPIO.LOW)
                print("Fan off")
            time.sleep(delay)

    def get_gpu_temperature(self):
        ''' Return the GPU temperature in °C using vcgencmd
        '''
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        output, _error = process.communicate()
        return float(output[output.index('=') + 1:output.rindex("'")])

if __name__ == "__main__":
    rpi_fan = Rpi_fan(target_temp = 45, pin = 24)
    rpi_fan.run(delay = 10)
