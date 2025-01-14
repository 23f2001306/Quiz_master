from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pswd = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    name = StringField('Full Name', validators=[InputRequired()])
    qualification = StringField('Qualification',validators=[InputRequired()])
    dob =  DateField('Date of Birth',format='%d-%m-%Y', validators=[InputRequired()])
    submit = SubmitField('Signup')