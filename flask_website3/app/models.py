from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def __repr__(self):
        return '<User {}>'.format(self.username)


class UserPreference(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64), index=True, unique=True)
    lastname = db.Column(db.String(64), index=True, unique=True)
    gender = db.Column(db.String(64), index=True, unique=True)
    age = db.Column(db.Integer, index=True)
    weight_lb = db.Column(db.Integer, index=True)
    height_in = db.Column(db.Integer, index=True)
    foods_allergic = db.Column(db.String(1200), index=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
