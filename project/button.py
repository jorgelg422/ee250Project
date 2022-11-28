import time
import grovepi
import requests

from grove_rgb_lcd import *
import grovepi
import grove_rgb_lcd as lcd

# Connect the Grove Button to digital port D3
button = 3
# Connect the Grove Green LED to digital port D2
led_green = 2
# Connect the Grove Red LED to digital port D4
led_red = 4


# Setup
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(led_green,"OUTPUT")
grovepi.pinMode(led_red,"OUTPUT")
time.sleep(1)

deviceSelect = 0
greenOn = 0
c = 0

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
                if (greenOn == 0):      # if it is off, turn it on
                    grovepi.digitalWrite(led_green,1)
                elif (greenOn == 1):    # if it is on, turn it off
                    grovepi.digitalWrite(led_green,0)
                greenOn = (greenOn + 1)%2
                # add tempo data (beats / min)              # TODOOOO
                tempo = 149 #TEST NUMBER
                time_between_blinks = 60.0 / tempo
                time.sleep(time_between_blinks)
                # lcd constantly changes colors if song is playing
                setRGB(c,255-c,0)
                if (c==254):
                    c = 0
                else:
                    c = c + 1
                # Check if button is pressed
                if grovepi.digitalRead(button):
                    (deviceSelect==0)
        elif (deviceSelect==1): # paused
            #response = requests.get('https://127.0.0.1:5000/me/player/pause')
            # green LED should be off
            grovepi.digitalWrite(led_green,0)
            # red LED should be on
            grovepi.digitalWrite(led_red,1)
            # lcd should be red
            setRGB(136,8,8)
            # display "PAUSED" on LCD
            setText("Spotify\nPAUSED")
        time.sleep(1)

    except IOError:
        print ("Error")
