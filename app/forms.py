from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField,TextAreaField,SelectField,RadioField
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


class CreateChapForm(FlaskForm):
    subject_id = SelectField('Select Subject', coerce=int, validators=[DataRequired()])
    chap_name1 = StringField("Chapter Name",validators= [DataRequired()])
    chap_description1 = TextAreaField("Description",validators= [DataRequired()])
    submit = SubmitField("Create Chapter")   


class ChapForm(FlaskForm):
    chap_name = StringField("Chapter Name",validators= [DataRequired()])
    chap_description = TextAreaField("Description",validators= [DataRequired()])

class CreateQuizForm(FlaskForm):
    chap_id1 = SelectField('Select Chapter', coerce=int, validators=[DataRequired()])
    quiz_name1 = StringField("Quiz Name",validators= [InputRequired()])
    date_of_quiz1 = DateField('Date of Quiz',format="%Y-%m-%d", validators=[InputRequired()])
    time_duration1 = StringField('Time Duration', validators=[InputRequired()])
    remarks1 = TextAreaField("Remarks",validators= [DataRequired()])

    submit = SubmitField("Create Quiz")


class QuizForm(FlaskForm):
    quiz_name = StringField("Quiz Name",validators= [InputRequired()])
    date_of_quiz = DateField('Date of Quiz',format="%Y-%m-%d", validators=[InputRequired()])
    time_duration = StringField('Time Duration', validators=[InputRequired()])
    remarks = TextAreaField("Remarks",validators= [DataRequired()])

class SelectQuizForm(FlaskForm):
    quiz_id = SelectField("Select a Quiz", coerce=int, validators=[DataRequired()])

class AddQtnForm(FlaskForm):
    question_statement = TextAreaField("Question",validators=[DataRequired()])
    option1 = StringField("Option 1",validators=[DataRequired()])
    option2 = StringField("Option 2",validators=[DataRequired()])
    option3 = StringField("Option 3",validators=[DataRequired()])
    option4 = StringField("Option 4",validators=[DataRequired()])
    correct_option = SelectField("Correct Option",choices=[(1, 'Option 1'),(2, 'Option 2'),(3, 'Option 3'),(4, 'Option 4')],validators=[DataRequired()],
                                 render_kw={"class": "form-select","style": "width: 200px;"})
    

class AttendQuizForm(FlaskForm):
    answer = RadioField("Choose an answer")


