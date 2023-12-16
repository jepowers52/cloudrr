"""CRUD operations."""

from model import db, User, Animal, Pet, connect_to_db


def create_user(username, email, password):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password)

    return user



def get_user_by_id(user_id):
    """Return a user by id."""
    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_animal(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    animal = Animal(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path,
    )
    return animal


def get_animals():
    return Animal.query.order_by('name').all()


def get_animal_by_id(movie_id):
    return Animal.query.get(movie_id)


def create_pet(user_id, animal_id, pet):
    """Create and return new pet rating."""
    new_pet = Pet(
        user_id=user_id,
        animal_id=animal_id,
        pet=pet
    )

    return new_pet

def get_rating_by_user_and_animal(user_id, animal_id):
    """Returns a raiting based off user_id and animal_id"""

    return Pet.query.filter(Pet.user_id ==user_id,  Pet.animal_id == animal_id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)