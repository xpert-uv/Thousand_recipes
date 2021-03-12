from flask import Flask, request, render_template, redirect, session
from model import db, connect_db, User, Food, Cocktails, Wine, Wineparing
import keys
import os
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', keys.database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get(keys.SECRET_KEY, 'SQLALCHEMY')

connect_db(app)
