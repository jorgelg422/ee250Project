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
#import mailboxManager

app = Flask('Spotify project')

"""
The @app.route() above the function is called a decorator. We will skip
explaining decorators in detail for brevity. The functions below, such as
get_mailbox_callback(), are callbacks that get called when certain types
of HTTP request are received by the Flask server. With the decorator's
input arguments below and the Flask server initialization in
if __name__ == '__main__':, this first callback is set to be specifically
called when a GET request is sent to the URL "http://0.0.0.0:[port]/mailbox"
"""

CLIENT_ID = "e26cfa66c29f45dbb775d2c83bb5c068"
CODE = "AQDNKGIrvRMLoldeVxL1euBhPnRX4Bvw6QnTgrSs7hqjokGqvsFm8384nREY7kFwqF9J8m8poOEmh0z_XOteQifMdeLUOeylQJ_jZvPshTgeok9-IZbiSgkJ7E6P__pVawPD6nb4igEU5UxsQ0S9UnjEkhhdz8DaNsWdUP701-49Xpfk4R4-zYl2X3_3-cJ-BLFuljjAss-CKlb20dmW-1eRqQQqXgwkXEAN0vnMmrig5hWeGg_WgP4oXyU8i1XxdbyyY-JDgYCHrJ-iizuxQpdmuoygx4cz4u8Bn3i7Ec42DCkBaT32iPMVWw"
CLIENT_SECRET = "036ab0fdff5340439baaa988cb917a2f"
ACCESS_TOKEN = 'BQAaDP7Pe1z2nAJRZkIlJEq-LV711Zt7crpmnKwGc6pMybTU9q8SOkk80Sq4cMA6pFVkpa3KOZ2A3DYw3Xj06XisvQST1H7NDEGPfUDLA2DRWWfKx6BM2HSnxSPKuLjUbNufczxbnClRuOhkZes00tl7Z72IR2XJ7Q0e96lyfOiLjlvQcVxbQKJdHKChH1Uhkw'
REFRESH_TOKEN = 'AQBddtd60GEeGMDRlzUY8yQUlARrEZ0bRL42h_iYDArGUZB2nPld7ydtoWGS9SJOPxqnA7zDe_MVD8HnhJXVkQv0eNuX764p8h95q1IJESK5LqHE6bmTY2sP36yEqb6TjqM'
SONG_ID = "spotify:album:4uJ318DIOMiA4y9vg2dRwv"

PHONE_ID = "e0d5d19b595448784be6944aff73d23ceed58c6a"

@app.route('/')
def home():
    return(render_template('home.html'))

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
    #webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(params))
    #response = requests.get("https://accounts.spotify.com/authorize?client_id=e26cfa66c29f45dbb775d2c83bb5c068&response_type=code&redirect_uri=http://127.0.0.1:5000")
    # if(response.status_code==200):
    #     print(response.text)
    # else:
    #     print(response.text)
    #     #print("Basic "+IDSecretEncoded.decode())

    return(render_template('home.html'))
    #return

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
         'type' : 'album',
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
        data = data['albums']['items'][1]
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

    IDSecret = CLIENT_ID+':'+CLIENT_SECRET
    IDSecretEncoded = base64.b64encode(IDSecret.encode())
    headers = {
        'Authorization' : f"Bearer {ACCESS_TOKEN}",
        'Content-Type' : 'application/json'
    }
    params = {
        'context_uri' : "spotify:album:4uJ318DIOMiA4y9vg2dRwv",
        'device_id' : PHONE_ID
    }

    response = requests.put("https://api.spotify.com/v1/me/player/play", params=params, headers=headers)
    return(render_template('home.html'))

@app.route('/me/player/pause')
def pauseSong():

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
if __name__ == '__main__':
    # Set up argparse, a Python module for handling command-line arguments
    parser = argparse.ArgumentParser(prog='mailServer',
            description='Script to start up mail server')

    # parser.add_argument('-p', metavar='password', required=True,
    #         help='Required password to access server')

    # args = parser.parse_args()

    # mailbox_password = args.p   # password
    # mailbox_manager = mailboxManager.mailboxManager()

    app.run(debug=False, host='0.0.0.0', port=5000)

