"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()



class User(UserMixin, db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    pet_ratings = db.relationship("User_pet_rating", back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User id={self.id} username={self.username}>'
    
    

class Animal(db.Model):
    """"An animal."""
    
    __tablename__ = "animals"

    animal_id = db.Column(db.String, primary_key=True, unique=True)
    species = db.Column(db.String)
    location = db.Column(db.String)   
    age = db.Column(db.String)  #ex: young
    name = db.Column(db.String)
    image = db.Column(db.String)    #url
    petfinder_link = db.Column(db.String)   #url
    
    pet_ratings = db.relationship("User_pet_rating", back_populates='animal')


    def __repr__(self):
        return f"<Animal animal_id={self.animal_id} name={self.name}>"



class User_pet_rating(db.Model):
    """A rating of Pet or Pass."""


    __tablename__ = "user_pet_ratings"
    
    pet_rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey("users.id"))
    animal_id = db.Column(db.String, db.ForeignKey("animals.animal_id"))
    pet_rating = db.Column(db.String)
    
    user = db.relationship("User", back_populates='pet_ratings')
    animal = db.relationship("Animal", back_populates='pet_ratings')

    def __repr__(self):
        return f"<User_pet_rating pet_rating_id={self.pet_rating_id} pet_rating={self.pet_rating}>"




def connect_to_db(flask_app, db_uri="postgresql:///cloudrrDB", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
