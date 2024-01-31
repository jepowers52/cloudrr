"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    pet_ratings = db.relationship("User_pet_rating", back_populates='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
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
