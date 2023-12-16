"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# update blanks!
class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'

class Animal(db.Model):
    """"An animal."""
    
    __tablename__ = "animals"

    animal_id = db.Column(db.String, primary_key=True)
    species = db.Column(db.String)
    location = db.Column(db.String)   # state from animal address 
    age = db.Column(db.String)  #ex: young
    name = db.Column(db.String)
    image = db.Column(db.String)    #url
    petfinder_link = db.Column(db.String)   #url

    
    

    def __repr__(self):
        return f"<Animal animal_id={self.animal_id} name={self.name}>"



class Pet(db.Model):
    """A rating of Pet or Pass."""


    __tablename__ = "pets"
    
    pet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    animal_id = db.Column(db.Integer, db.ForeignKey("animals.animal_id"))
    pet = db.Column(db.Boolean)
    

    def __repr__(self):
        return f"<Pet pet_id={self.pet_id} pet={self.pet}>"




def connect_to_db(flask_app, db_uri="postgresql:///pets", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
