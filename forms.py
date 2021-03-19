from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, InputRequired, Email


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(
        min=6, message="Username must be 6 character long")])
    password = PasswordField("Password", validators=[InputRequired(), Length(
        min=8, message="Password must be 8 character long")])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email",  [InputRequired("Please enter your email address."), Email(
        "This field requires a valid email address")])
