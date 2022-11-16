from flask import Flask, render_template
from flask import jsonify
from flask import request

import requests
import argparse
import json
import socket
import base64
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
CODE = "AQCz0aWk9UkCizhClkNnpyJZvmuA4LDb4VTfBv71I7JnlV0SRZ7chF2MMjP3ywLHZ_Dy-EojPUDGSNVv9C_fSI403jovwOztsm8k5P3i1GnpT75CzLMMHxUQwklgszQEiGcLPJWypkUOcOx1CQRhGgz6Kos2Y_MQ5g"
CLIENT_SECRET = "036ab0fdff5340439baaa988cb917a2f"
ACCESS_TOKEN = 'BQDa6uKc6ZtVbCZ1ywRc_UEwHKLJ6DhcRyrvpmDfcE4q2_-YXqRh81K-XGRAQbYUHXaoPPCcY5focAlJzzmGti1CkoMN8vhJ14a0Efs7kNk1uzk4BUF514AXbkImN3kVjmnEDCoJT3judqeTvnc3b8pnvnx62ETn9uG4GKrmvVbxx3HNvz4'

@app.route('/')
def home():
    return(render_template('home.html'))

@app.route('/callback')
def authorize():

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
         'track' : 'Perfect',
         'artist' : 'Ed Sheeran'
    }

    headers = {
        'Authorization' : ACCESS_TOKEN,
        'Content-Type' : 'application/json'
    }

    #response = requests.get("https://accounts.spotify.com/authorize?client_id="+CLIENT_ID+"&response_type=code&redirect_uri=127.0.0.1:5000/")
    response = requests.get("https://accounts.spotify.com/search", params=params,headers=headers)
    if(response.status_code==200):
        data = response.json()
        print(data)
    else:
        print(response.text)
        #print("Basic "+IDSecretEncoded.decode())

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

