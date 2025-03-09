from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField,TextAreaField
from wtforms.validators import InputRequired, EqualTo, DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')
    
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pswd = PasswordField('Confirm Password', validators=[InputRequired(),EqualTo('password',message="Passwords must match.")])
    name = StringField('Full Name', validators=[InputRequired()])
    qualification = StringField('Qualification',validators=[InputRequired()])
    dob =  DateField('Date of Birth',format="%Y-%m-%d", validators=[InputRequired()])
    submit = SubmitField('Signup')

class SubForm(FlaskForm):
    sub_name = StringField("Subject Name",validators= [DataRequired()])
    sub_description = TextAreaField("Description",validators= [DataRequired()])

class CreateSubForm(FlaskForm):
    sub_name1 = StringField("Subject Name",validators= [DataRequired()])
    sub_description1 = TextAreaField("Description",validators= [DataRequired()])
    submit = SubmitField("Create Subject")   

class SearchSubForm(FlaskForm):
    sub_name = StringField("Search Subject",validators= [InputRequired()])
    search = SubmitField("Search")


