from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import Users


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('sign in')


class RegistrationForm(FlaskForm):
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
        for val in phone_number.data:
            if val not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                raise ValidationError('Invalid phone number')
        if len(phone_number.data) > 13:
            raise ValidationError('Phone number too long')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    county = StringField('County', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[DataRequired()])
    submit = SubmitField('submit')


class PlaceOrderForm(FlaskForm):
    id = StringField('Enter ID to place order', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FilterSellersForm(FlaskForm):
    county = StringField('Filter using county', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CheckOrderForm(FlaskForm):
    id = StringField('Enter Id', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeleteOrdersForm(FlaskForm):
    id = StringField('Enter ID to delete', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MessageForm(FlaskForm):
    content = TextAreaField("message content", validators=[DataRequired()])
    to = StringField("receiver", validators=[DataRequired()])
    submit = SubmitField('Submit')
