"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from model import connect_to_db, db
from model import User
import crud
from jinja2 import StrictUndefined
import os
import requests
import json
import petfinder



app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager(app)
login_manager.view = '/login_page'

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
    age = request.args.get('animal-age')
    gender = request.args.get('animal-gender')
    color = request.args.get('animal-color')
    coat = request.args.get('animal-coat')
    

    url = 'https://api.petfinder.com/v2/animals'
    payload = {'type' : type,
               'location' : location, 
               'age' : age,
               'color' : color,
               'gender' : gender,
               'coat' : coat


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
@login_required 
def userbio():
    

    ratings = crud.get_ratings_by_user(current_user.email)
    #  TODO:
    # for each rating in Ratings
    # find the pet rating, Animal's name, Animal's photo, Animal's petfinder link 

    return render_template('user-bio.html', ratings=ratings)


"""************* LOG IN / LOG OUT *************"""
@app.route("/login-page")
def login_page():
    """Process user login."""
    # , methods=["POST"]
    # email = request.form.get("email")
    # password = request.form.get("password")

    # user = crud.get_user_by_email(email)
    # # breakpoint()
    
    # if not user or user.password != password:
    #     flash("The email or password you entered was incorrect.")
    # else:
    #     # Log in user by storing the user's email in session
    #     session["user_email"] = user.email
    #     flash(f"Welcome back, {user.email}!")
    
    # return redirect("/")
    return render_template('login-page.html')

@login_manager.user_loader
def load_user(id):
    return crud.get_user_by_userid(id)

@app.route("/login", methods=["POST"])
def user_login():
    if current_user.is_authenticated:
        return redirect("/")
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if user:
        if user.check_password(password):
            login_user(user)
            return redirect('/')
        flash("The email or password you entered was incorrect.")
        return redirect('/login')
    else:
        flash("The email or password you entered was incorrect.")
        return redirect('/login')
        
@app.route("/create-user", methods=["POST"])
def create_user():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    crud.create_user(username, email, password)
    flash(f"Welcome {username}!")
    return redirect('/login')

@app.route('/logout')
@login_required 
def user_logout():
    logout_user()
    flash(f"Goodbye!")
    return redirect('/')

@app.route("/animal-types")
def retrieve_animal_types():
    with open("data/animal-types.json") as f:
        animal_type_data = json.loads(f.read())
        animal_type_json = json.dumps(animal_type_data)
        # animal_type_data = f.read()
    # print(animal_type_json)
    # animal_type_data = open("data/animal-types.json")
    return animal_type_json

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


