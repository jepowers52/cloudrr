"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
import requests
import json
import petfinder



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
    access_token = petfinder.obtain_access_token()
    return access_token


@app.route("/animal-search")
def animal_search_request():
    type = request.args.get('species')
    location = request.args.get('animal-location')
    age = request.args.get('animal_age')
   
    url = 'https://api.petfinder.com/v2/animals'
    payload = {'type' : type,
               'location' : location, 
               'age' : age
    }
    access_token = request_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}

    res = requests.get(url, headers=headers, params=payload)
    animal_search_results = res.json()

    return render_template('search-results.html',
                           results=animal_search_results
                           )

@app.route("/postman-test")
def postman():
    url = "https://api.petfinder.com/v2/animals"

    payload = {'type' : 'Dog',
               'location' : 'OR', 
               'age' : 'Adult'
    }
    headers = {
        'Authorization': 'Bearer ' #add access token when testing
    }

    response = requests.request("GET", url, headers=headers, params=payload)

    return response.json()


@app.route("/store-user-rating", methods=["POST"])
def store_user_rating():
    """Add User rating to Database"""

    crud.store_user_rating(request)


    return {"success" : "something"}

@app.route("/user-bio")
def userbio():
    
    if "user_email" in session:
        
        ratings = crud.get_ratings_by_user()
        #  TODO:
        # for each rating in Ratings
        # find the pet rating, Animal's name, Animal's photo, Animal's petfinder link 
 
        return render_template('user-bio.html', ratings=ratings)

    else:
        flash("Please login to view user history.")
        return render_template('homepage.html')

@app.route("/login")
def user_login():

    return

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    # breakpoint()
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
    
    return redirect("/")

@app.route("/animal-types")
def retrieve_animal_types():
    # with open("data/animal-types.json") as f:
    #     animal_type_data = json.loads(f.read())
        # animal_type_data = f.read()
        
    # animal_type_data = open("data/animal-types.json")
    return json.loads(open("data/animal-types.json"))

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


