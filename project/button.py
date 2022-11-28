import time
import grovepi
import requests

from grove_rgb_lcd import *
import grovepi
import grove_rgb_lcd as lcd

# Connect the Grove Button to digital port D3
button = 3
# Connect the Grove Green LED to digital port D4
led_green = 2
# Connect the Grove Red LED to digital port D5
led_red = 4

#lcd.setRGB(0, 128, 0)

# Setup
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(led_green,"OUTPUT")
grovepi.pinMode(led_red,"OUTPUT")
deviceSelect = 0

while True:
    try:

        # Check if button is pressed
        if grovepi.digitalRead(button):
            # then device is switched play/paused
            deviceSelect = (deviceSelect + 1)%2
            if (deviceSelect==0):   # playing
                #response = requests.get('http://127.0.0.1:5000/me/player/play')
                while (deviceSelect==0):
                    # red LED should be off
                    grovepi.digitalWrite(led_red,0)
                    # display title of selected song
                    setText("song title")
                    # blink green LED according to tempo of selected song
                    grovepi.digitalWrite(led_green,1)
                    # add tempo data (beats / min)              # TODOOOO
                    tempo = 149 #TEST NUMBER
                    time_between_blinks = 60.0 / tempo
                    time.sleep(time_between_blinks)
                    # Check if button is pressed
                    if grovepi.digitalRead(button):
                        (deviceSelect==0)
            elif (deviceSelect==1): # paused
                #response = requests.get('https://127.0.0.1:5000/me/player/pause')
                # green LED should be off
                grovepi.digitalWrite(led_green,0)
                # display "PAUSED" on LCD
                setText("Spotify\nPAUSED")
        time.sleep(1)

    except IOError:
        print ("Error")
