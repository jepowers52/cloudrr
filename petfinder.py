import os
import requests

API_KEY = os.environ['PETFINDER_KEY']
API_SECRET = os.environ['PETFINDER_SECRET']


def obtain_access_token():
    """Post request to API to provide access token"""
    
    url = "https://api.petfinder.com/v2/oauth2/token"

    payload = f'grant_type=client_credentials&client_id={API_KEY}&client_secret={API_SECRET}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    access_results = response.json()

    return access_results['access_token']


def get_animal_data(animal_id):
    """search API for specific individual animal
       Example: 'animal_id': '70427330'"""

    animal_url = f"https://api.petfinder.com/v2/animals/{animal_id}"

    access_token = obtain_access_token()

    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.request("GET", animal_url, headers=headers)

    print(response.json())
    
    return response.json()