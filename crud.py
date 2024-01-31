"""CRUD operations."""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session
import model
from model import db, User, Animal, User_pet_rating, connect_to_db
import requests
# import server
import os
import json
import petfinder

# db = SQLAlchemy()
# model.connect_to_db(server.app)

def create_user(username, email, password):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password)
    return user



def get_userid_by_username(username):
    """Return a user by username."""

    user = User.query.filter_by(username=username).first()
    return user.user_id

def get_userid_by_email(email):

    user = User.query.filter_by(email=email).first()
    return user.user_id

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter_by(email=email).first()


def create_animal(animal_id, species, location, age, name, image, petfinder_link):
    """Create and return a new animal."""
    animal = Animal(
        animal_id=animal_id,
        species=species,
        location=location,
        name=name,
        image=image,
        petfinder_link=petfinder_link,
    )
    return animal



def get_animal_by_id(animal_id):
    return Animal.query.filter_by(animal_id=animal_id).first()


def create_pet_rating(user_id, animal_id, pet_rating):
    """Create and return new pet rating from test data."""
    new_pet = User_pet_rating(
        user_id=user_id,
        animal_id=animal_id,
        pet_rating=pet_rating
    )

    return new_pet



def store_user_rating(user_rating_JSON):
    """Store user rating in the Database
    ex: {'button_value': 'Pet', 'animal_id': '70400762'}
    """
    user_id = 1 #hardcoded for testing
    animal_id = user_rating_JSON.json["animal_id"]
    pet_rating = user_rating_JSON.json["button_value"]


    new_animal = petfinder.get_animal_data(animal_id)
    add_animal_to_db(new_animal)

    new_rating = create_pet_rating(user_id, animal_id, pet_rating)
    
    model.db.session.add(new_rating)
    model.db.session.commit() 
    
def get_ratings_by_user():
    user_email = session["user_email"] 
    user_id = get_userid_by_email(user_email)
    user_ratings = User_pet_rating.query.filter_by(user_id=user_id).all()
    
    print(user_ratings)
    return user_ratings


    

def add_animal_to_db(animal_json):
    """Ad animal to db if not already included"""
    animal_id, species, location, age, name, image, petfinder_link = (
        animal_json["animal"]["id"],
        animal_json["animal"]["type"],
        animal_json["animal"]["contact"]["address"]["state"],
        animal_json["animal"]["age"],
        animal_json["animal"]["name"],
        animal_json["animal"]["photos"][0]["medium"],
        animal_json["animal"]["url"]
        )

    if not Animal.query.filter(Animal.animal_id == f'{animal_id}').all():
        db_animal = create_animal(animal_id, species, location, age, name, image, petfinder_link)
        
        model.db.session.add(db_animal)
        model.db.session.commit()    

if __name__ == '__main__':
    from server import app
    connect_to_db(app)