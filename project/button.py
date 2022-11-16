import time
import grovepi
import requests

# Connect the Grove Button to digital port D3
# SIG,NC,VCC,GND
button = 3

# Setup
grovepi.pinMode(button,"INPUT")
deviceSelect = 0
while True:
    try:
        # Check for input
        if grovepi.digitalRead(PORT_BUTTON):
            deviceSelect = (deviceSelect + 1)%2
            if(deviceSelect==0):
                response = requests.get('http://127.0.0.1:5000/me/player/play')
            else:
                response = requests.get('https://127.0.0.1:5000/me/player/pause')
        time.sleep(.5)

    except IOError:
        print ("Error")