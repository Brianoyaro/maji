from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from app.models import Users


class EditProfileForm(FlaskForm):
    """form for profile editing"""
    username = StringField('Username', validators=[DataRequired()])
    county = StringField('County', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[DataRequired()])
    profile_pic = FileField("Edit profile picture", validators=[FileAllowed(["jpg","png"])])
    submit = SubmitField('submit')
    
    def validate_phone_number(self, phone_number):
        """ensures user enters right format for a phone number"""
        for val in phone_number.data:
            if val not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                raise ValidationError('Invalid phone number')
        if len(phone_number.data) > 13:
            raise ValidationError('Phone number too long')


class PlaceOrderForm(FlaskForm):
    """form for placing an order"""
    id = StringField('Enter ID to place order', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FilterSellersForm(FlaskForm):
    """form for filtering users using their county when placing an order"""
    county = StringField('Filter using county', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CheckOrderForm(FlaskForm):
    """form that checks an order using its id"""
    id = StringField('Enter Id', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeleteOrdersForm(FlaskForm):
    """form that deletes an order using its id"""
    id = StringField('Enter ID to delete', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MessageForm(FlaskForm):
    """form that receieves text message"""
    content = TextAreaField("message content", validators=[DataRequired()])
    to = StringField("receiver", validators=[DataRequired()])
    submit = SubmitField('Submit')

