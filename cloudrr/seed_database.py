"""Script to seed database."""

import os
import json
# from random import choice, randint
# from datetime import datetime

import crud
import model
import server

os.system("dropdb cloudrrDB")
os.system('createdb cloudrrDB')

model.connect_to_db(server.app)
model.db.create_all()

############################ animals ########################################

with open('data/test-animal-data.json') as file1:
    animal_data = json.loads(file1.read())


animals_in_db = []
for animal in animal_data:
    animal_id, species, location, age, name, image, petfinder_link = (
        animal["animal_id"],
        animal["species"],
        animal["location"],
        animal["age"],
        animal["name"],
        animal["image"],
        animal["petfinder_link"],
        )

    db_animal = crud.create_animal(animal_id, species, location, age, name, image, petfinder_link)
    animals_in_db.append(db_animal)

model.db.session.add_all(animals_in_db)
model.db.session.commit()    

############################ users ########################################

with open('data/test-user-data.json') as file2:
    user_data = json.loads(file2.read())


users_in_db = []
for user in user_data:
    username, email, password = (
        user["username"],
        user["email"],
        user["password"],
    )
    db_user = crud.create_user(username, email, password)
    users_in_db.append(db_user)

model.db.session.add_all(users_in_db)
model.db.session.commit() 

############################## pet ratings ######################################

with open('data/test-pet-data.json') as file3:
    pet_rating_data = json.loads(file3.read())

    # { "username": "user2",
    # "animal_id": "dog-004",
    #  "pet": "FALSE"},

pet_ratings_in_db = []

for rating in pet_rating_data:

    username, animal_id, pet_rating = (
        rating["username"],
        rating["animal_id"],
        rating["pet_rating"],
    )


    # pet_rating = bool(pet_rating)
    user_id = crud.get_userid_by_username(username)

    db_pet_rating = crud.create_pet_rating(user_id, animal_id, pet_rating)
    pet_ratings_in_db.append(db_pet_rating)

model.db.session.add_all(pet_ratings_in_db)
model.db.session.commit() 

####################################################################

