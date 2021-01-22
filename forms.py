from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class Register(FlaskForm):
    """Form for registering a user."""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first = StringField("First Name", validators=[InputRequired()])
    last = StringField("Last Name", validators=[InputRequired()])

class Login(FlaskForm):
    """Form for logging in an existing user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])