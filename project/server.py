from flask import Flask, render_template
from flask import jsonify
from flask import request

import requests
import argparse
import json
import socket
import base64
import webbrowser
from urllib.parse import urlencode
import threading
from grove_rgb_lcd import *
import grovepi
import grove_rgb_lcd as lcd

app = Flask('Spotify project')


CLIENT_ID = "e26cfa66c29f45dbb775d2c83bb5c068"
CODE = "AQDNKGIrvRMLoldeVxL1euBhPnRX4Bvw6QnTgrSs7hqjokGqvsFm8384nREY7kFwqF9J8m8poOEmh0z_XOteQifMdeLUOeylQJ_jZvPshTgeok9-IZbiSgkJ7E6P__pVawPD6nb4igEU5UxsQ0S9UnjEkhhdz8DaNsWdUP701-49Xpfk4R4-zYl2X3_3-cJ-BLFuljjAss-CKlb20dmW-1eRqQQqXgwkXEAN0vnMmrig5hWeGg_WgP4oXyU8i1XxdbyyY-JDgYCHrJ-iizuxQpdmuoygx4cz4u8Bn3i7Ec42DCkBaT32iPMVWw"
CLIENT_SECRET = "036ab0fdff5340439baaa988cb917a2f"
ACCESS_TOKEN = 'BQDMhEpeoTCch69DGWHSC1lmiWhLpyflFFnVniJjXBpqs46jFPUt1DDQ9ovw2I7yj8pUUNJR9CCbJKyrF2cpTfUbfdy9-S4D5pQP6yUffnN9uv9fnzuADEitYd9DERVWG_mADIjeogU6AcXX_NgJlVXo74TtO1kzZjEkra5vdgHEyqxLngxP4u3Q7bqrv9H7XA'
REFRESH_TOKEN = 'AQBddtd60GEeGMDRlzUY8yQUlARrEZ0bRL42h_iYDArGUZB2nPld7ydtoWGS9SJOPxqnA7zDe_MVD8HnhJXVkQv0eNuX764p8h95q1IJESK5LqHE6bmTY2sP36yEqb6TjqM'
SONG_ID = "spotify:album:4uJ318DIOMiA4y9vg2dRwv"

PHONE_ID = "fd454582b6d009c5467dab05a7af1866f635e3f9"
COMPUTER_ID = "34d98f1a2e6bef776e931a035e35df0fd1008e24"

DEVICES = [PHONE_ID, COMPUTER_ID]

global deviceSelect 
deviceSelect = 1

@app.route('/')
def home():
    return(render_template('app.html'))

@app.route('/permissions')
def getCode():

    IDSecret = CLIENT_ID+':'+CLIENT_SECRET
    IDSecretEncoded = base64.b64encode(IDSecret.encode())

    params = {
        'client_id' : CLIENT_ID,
        'response_type' : 'code',
        'redirect_uri' : 'http://127.0.0.1:5000',
        'scope' : 'user-read-playback-state app-remote-control user-modify-playback-state user-read-currently-playing streaming'
    }

    return(render_template('home.html'))

@app.route('/callback')
def getAccessToken():

    IDSecret = CLIENT_ID+':'+CLIENT_SECRET
    IDSecretEncoded = base64.b64encode(IDSecret.encode())

    params = {
         'grant_type' : 'authorization_code',
         'code' : CODE,
         'redirect_uri' : 'http://127.0.0.1:5000'
    }

    headers = {
        'Authorization' : 'Basic '+(IDSecretEncoded.decode()),
        'Content-Type' : 'application/x-www-form-urlencoded'
    }


    #response = requests.get("https://accounts.spotify.com/authorize?client_id="+CLIENT_ID+"&response_type=code&redirect_uri=127.0.0.1:5000/")
    response = requests.post("https://accounts.spotify.com/api/token", params=params,headers=headers)
    if(response.status_code==200):
        data = response.json()
        print(data)
    else:
        print(response.text)
        #print("Basic "+IDSecretEncoded.decode())

    return(render_template('home.html'))

@app.route('/search')
def search():

    IDSecret = CLIENT_ID+':'+CLIENT_SECRET
    IDSecretEncoded = base64.b64encode(IDSecret.encode())

    params = {
         'type' : 'track',
         'include_external' : 'audio',
         'q' : "perfect Ed Sheeran"
    }

    headers = {
        'Authorization' : f"Bearer {ACCESS_TOKEN}",
        'Content-Type' : 'application/json'
    }

    response = requests.get("https://api.spotify.com/v1/search", params=params,headers=headers)
    if(response.status_code==200):
        data = response.json()
        data = data['tracks']['items'][0]
        myObj = json.dumps(data, indent=4)
        print(myObj)
        #print(formatStr)
    else:
        print(response.text)
        #print("Basic "+IDSecretEncoded.decode())

    return(render_template('home.html'))

@app.route('/refresh')
def refresh():

    IDSecret = CLIENT_ID+':'+CLIENT_SECRET
    IDSecretEncoded = base64.b64encode(IDSecret.encode())

    params = {
         'grant_type' : 'refresh_token',
         'refresh_token' : REFRESH_TOKEN,
    }

    headers = {
        'Authorization' : 'Basic '+(IDSecretEncoded.decode()),
        'Content-Type' : 'application/x-www-form-urlencoded'
    }


    #response = requests.get("https://accounts.spotify.com/authorize?client_id="+CLIENT_ID+"&response_type=code&redirect_uri=127.0.0.1:5000/")
    response = requests.post("https://accounts.spotify.com/api/token", params=params,headers=headers)
    if(response.status_code==200):
        data = response.json()
        print(data)
    else:
        print(response.text)
        #print("Basic "+IDSecretEncoded.decode())

    return(render_template('home.html'))


@app.route('/me/player/devices')
def getDevices():

    IDSecret = CLIENT_ID+':'+CLIENT_SECRET
    IDSecretEncoded = base64.b64encode(IDSecret.encode())

    headers = {
        'Authorization' : f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get("https://api.spotify.com/v1/me/player/devices", headers=headers)
    if(response.status_code==200):
        data = response.json()
        myObj = json.dumps(data, indent=4)
        print(myObj)
    else:
        print(response.text)

    return(render_template('home.html'))

@app.route('/me/player/play')
def playSong():
    global deviceSelect
    deviceSelect = 0
    #deviceSelect = (deviceSelect+1)%2
    IDSecret = CLIENT_ID+':'+CLIENT_SECRET
    IDSecretEncoded = base64.b64encode(IDSecret.encode())
    headers = {
        'Authorization' : f"Bearer {ACCESS_TOKEN}",
        'Content-Type' : 'application/json'
    }
    params = {
        'context_uri' : "spotify:album:3T4tUhGYeRNVUGevb0wThu",
        'device_id' : PHONE_ID
    }

    response = requests.put("https://api.spotify.com/v1/me/player/play", params=params, headers=headers)
    print(response.status_code)
    # data = response.json()
    # myObj = json.dumps(data, indent=4)
    # print(myObj)
    return(render_template('home.html'))

@app.route('/me/player')
def transfer():
    global deviceSelect
    deviceSelect = (deviceSelect+1)%2
    IDSecret = CLIENT_ID+':'+CLIENT_SECRET
    IDSecretEncoded = base64.b64encode(IDSecret.encode())
    DEVICE_IDS = [DEVICES[deviceSelect]]
    print(DEVICE_IDS)
    headers = {
        'Authorization' : f"Bearer {ACCESS_TOKEN}",
        'Content-Type' : 'application/json'
    }
    params = {
        'device_ids' : DEVICE_IDS,
        'play' : 'true'
    }
    data = {
        'context_uri' : "spotify:album:3T4tUhGYeRNVUGevb0wThu"
    }

    response = requests.put("https://api.spotify.com/v1/me/player", params=params, headers=headers, data=json.dumps(data))
    print(response.status_code)
    data = response.json()
    myObj = json.dumps(data, indent=4)
    print(myObj)
    return(render_template('home.html'))

@app.route('/me/player/pause') 
def pauseSong():
    global deviceSelect
    deviceSelect = 1
    IDSecret = CLIENT_ID+':'+CLIENT_SECRET
    IDSecretEncoded = base64.b64encode(IDSecret.encode())
    headers = {
        'Authorization' : f"Bearer {ACCESS_TOKEN}",
        'Content-Type' : 'application/json'
    }
    params = {
        'device_id' : PHONE_ID
    }

    response = requests.put("https://api.spotify.com/v1/me/player/pause", params=params, headers=headers)
    if(response.status_code!=204):
        print(response.status_code)
        data = response.json()
        myObj = json.dumps(data, indent=4)
        print(myObj)
    #else:
        #print(response.text)


    return(render_template('home.html'))

def main():
    global deviceSelect
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

    greenOn = 0
    c = 0

    while True:
        print(deviceSelect)
        try:
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
                        # then device is switched play/paused
                        deviceSelect = (deviceSelect + 1)%2

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

                # Check if button is pressed
                if grovepi.digitalRead(button):
                    # then device is switched play/paused
                    deviceSelect = (deviceSelect + 1)%2
            time.sleep(0.1)

        except IOError:
            print ("Error")



if __name__ == '__main__':
    x = threading.Thread(target=main)
    x.start()
    app.run(debug=False, host='0.0.0.0', port=5000)
