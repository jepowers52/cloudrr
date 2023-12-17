"""CRUD operations."""

from model import db, User, Animal, User_pet_rating, connect_to_db


def create_user(username, email, password):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password)

    return user



def get_user_by_username(username):
    """Return a user by username."""
    return User.query.get(username)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_animal(animal_id, species, location, age, name, image, petfinder_link):
    """Create and return a new movie."""
    animal = Animal(
        animal_id=animal_id,
        species=species,
        location=location,
        name=name,
        image=image,
        petfinder_link=petfinder_link,
    )
    return animal


def get_animals():
    return Animal.query.order_by('name').all()


def get_animal_by_id(movie_id):
    return Animal.query.get(movie_id)


def create_pet_rating(user_id, animal_id, pet_rating):
    """Create and return new pet rating."""
    new_pet = User_pet_rating(
        user_id=user_id,
        animal_id=animal_id,
        pet_rating=pet_rating
    )

    return new_pet

def get_rating_by_user_and_animal(user_id, animal_id):
    """Returns a raiting based off user_id and animal_id"""

    return User_pet_rating.query.filter(User_pet_rating.user_id ==user_id,  User_pet_rating.animal_id == animal_id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)