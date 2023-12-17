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

with open('data/test-animal-data.json') as file:
    animal_data = json.loads(file.read())


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

with open('data/test-animal-data.json') as f:
    movie_data = json.loads(f.read())


movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (
        movie["title"],
        movie["overview"],
        movie["poster_path"],
    )
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit() 

############################## pet ratings ######################################

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())


movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (
        movie["title"],
        movie["overview"],
        movie["poster_path"],
    )
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit() 

####################################################################

for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(user, random_movie, score)
        model.db.session.add(rating)

model.db.session.commit()