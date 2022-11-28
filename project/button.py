import time
import grovepi
import requests

from grove_rgb_lcd import *
import grovepi
import grove_rgb_lcd as lcd

# Connect the Grove Button to digital port D3
button = 3

lcd.setRGB(0, 128, 0)


# Setup
grovepi.pinMode(button,"INPUT")
deviceSelect = 0
while True:
    try:
        # Check for input
        if grovepi.digitalRead(button):
            deviceSelect = (deviceSelect + 1)%2
            if(deviceSelect==0):
                response = requests.get('http://127.0.0.1:5000/me/player/play')
            else:
                response = requests.get('https://127.0.0.1:5000/me/player/pause')
        time.sleep(.5)

    except IOError:
        print ("Error")