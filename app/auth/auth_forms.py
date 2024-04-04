from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import Users


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('sign in')


class RegistrationForm(FlaskForm):
    """registration form"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone_number = StringField('Phone number', validators=[DataRequired()])
    county = StringField('County', validators=[DataRequired()])
    type = RadioField('User Type', choices=[('buyer', 'Buyer'), ('seller', 'Seller')], validators=[DataRequired()])
    submit = SubmitField('register')


    def validate_email(self, email):
        """to make sure email is unique before storing in database"""
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email')


    def validate_phone_number(self, phone_number):
        """ensure user typed corect phone number"""
        for val in phone_number.data:
            if val not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                raise ValidationError('Invalid phone number')
        if len(phone_number.data) > 13:
            raise ValidationError('Phone number too long')


class ResetRequestForm(FlaskForm):
    """form for requesting password change"""
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


class ActualRequestForm(FlaskForm):
    """form which receives user password update during password reset"""
    password = StringField("Password", validators=[DataRequired()])
    password2 = StringField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")
