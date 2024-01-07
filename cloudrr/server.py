"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
import requests

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['PETFINDER_KEY']
API_SECRET = os.environ['PETFINDER_SECRET']


@app.route("/")
def homepage():
    
    return render_template('homepage.html')


@app.route("/search")
def searchpage():
    return render_template('search.html')

@app.route("/request-access-token",  methods=['POST'])
def request_access_token():
    # post request to API to provide access token. access token needs to be added into the header of all requests 
    # "grant_type=client_credentials&client_id={CLIENT-ID}&client_secret={CLIENT-SECRET}" https://api.petfinder.com/v2/oauth2/token
    
    url = "https://api.petfinder.com/v2/oauth2/token"

    payload = f'grant_type=client_credentials&client_id={API_KEY}&client_secret={API_SECRET}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    access_results = response.json()
    print(type(response))
    print(access_results['access_token'])
    return access_results['access_token']

@app.route("/animals")
# DO THIS IN POSTMAN
def animal_search_request():
    type = request.args.get('species')
    location = request.args.get('animal-location')
    age = request.args.get('animal_age')
    # BLOCKED - how to add a header in a GET request to hold access token?

    url = 'https://api.petfinder.com/v2'
    payload = {'type' : type,
               'location' : location, 
               'age' : age
    }
    access_token = request_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    #response = requests.request("GET", url, headers=headers, data=payload)
    # "https://api.petfinder.com/v2/animals?type=Dog&age=Adult&location=OR"
    res = requests.get(url, headers=headers, data=payload)
    # print(type(res))
    print(res)
    animal_results = res.json()

    return animal_results

@app.route("/user-bio")
def userbio():
    return render_template('user-bio.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


