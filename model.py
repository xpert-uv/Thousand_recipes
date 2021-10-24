from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)

    food = db.Column(db.Integer, db.ForeignKey(
        "foodrecipes.id"))

    def __repr__(self):
        return f'< user id ={self.id}, username = {self.username}, first_name={self.first_name}, last_name={self.last_name}>'

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hashed_passwd = bcrypt.generate_password_hash(password).decode("utf8")
        return cls(username=username, password=hashed_passwd, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False


def passwordhash(password):
    hashed_passwd = bcrypt.generate_password_hash(password).decode("utf8")
    return hashed_passwd


class Food(db.Model):

    __tablename__ = "foodrecipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dish_id = db.Column(db.Integer, unique=True)
    dish_name = db.Column(db.Text)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instruction = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    image_url = db.Column(db.Text, nullable=False,
                          default="https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80")

    def __repr__(self):
        return f'< Recipe id = {self.id},dish_id ={self.dish_id}, dish name = {self.dish_name}, description = {self.description}, ingredients = {self.ingredients}, instruction = {self.instruction}, prep time = {self.prep_time}, total time = {self.total_time}, image = {self.image_url} >'
