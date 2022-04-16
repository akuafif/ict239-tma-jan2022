from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import Email, Length, InputRequired, DataRequired
from wtforms.widgets import PasswordInput
from wtforms_components import DateRange

class RegForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    #password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=20)])

    # Need to pass hide_value=False in order for the remember me function to work
    password = StringField('Password', validators=[InputRequired(), Length(min=5, max=20)], widget=PasswordInput(hide_value=False))
    name = StringField('Name')