from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, InputRequired
from app.models import User, System, Habit
from flask_login import current_user


'''                                                

        Stores all the classes needed to create forms 

'''                       


'''Existing User Login'''
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In') 



'''New Users Registration'''
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')


'''Create a new system'''
class SystemCreation(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    descr = TextAreaField('Some words of encouragement goes here', validators=[DataRequired()])
    submit = SubmitField('Save')


    

'''Create a new habit'''
class HabitCreation(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    systemID = SelectField('Select System', coerce=int, validators=[InputRequired()])
    goal = IntegerField('Frequency Goal', validators=[DataRequired()])
    submit = SubmitField('Save')



