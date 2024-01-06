"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['PETFINDER_KEY']
API_SECRET = os.environ['PETFINDER_SECRET']

location_states = ["AL", "KY", "OH", "AK", "LA", "OK", "AZ","ME", "OR", "AR", "MD",
                    "PA", "AS", "MA", "CA", "MI", "RI", "CO", "MN", "SC", "CT", "MS", 
                    "SD", "DE", "MO", "TN", "DC", "MT", "TX", "FL", "NE", "GA", 
                    "NV", "UT", "NH", "VT", "HI", "NJ", "VA", "ID", "NM", "VI", "IL",
                    "NY", "WA", "IN", "NC", "WV", "IA", "ND", "WI", "KS", "WY"]


@app.route("/")
def homepage():
    
    return render_template('homepage.html')


@app.route("/search")
def searchpage():
    return render_template('search.html', location_states=location_states)

@app.route("/request-acess-token", "POST")
def request_access_token():
    # post request to API to provide access token. access token needs to be added into the header of all requests 
    # "grant_type=client_credentials&client_id={CLIENT-ID}&client_secret={CLIENT-SECRET}" https://api.petfinder.com/v2/oauth2/token
    #
    pass # return access_token

@app.route("/animal-search")
# DO THIS IN POSTMAN
def animal_search_request():
    species = request.args.get('species')
    location_state = request.args.get('location_state')
    animal_age = request.args.get('animal_age')


    url = 'https://api.petfinder.com/v2/animals'
    payload = {type=species,
               location=location_state,
               age=animal_age
    }

    return f"""<!doctype html>
    <html>
    <head>
      <title>Results</title>
    </head>
    <body>
      Species: {species}, Location: {location_state}, Age: {animal_age}
    </body>
    </html>
    """

@app.route("/user-bio")
def userbio():
    return render_template('user-bio.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


