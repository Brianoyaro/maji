from flask import current_app
from time import time
import jwt
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    county = db.Column(db.String(30))
    phone_number = db.Column(db.String(13))
    password_hash = db.Column(db.String(128))
    type = db.Column(db.String(10))
    profile_pic = db.Column(db.String(40), nullable=False, default="default.jpg")
    orderee = db.relationship("Order", foreign_keys='Order.buyer_name', backref='purchaser', lazy="dynamic")
    ordered_to = db.relationship("Order", foreign_keys='Order.seller_id', cascade="all, delete-orphan", backref='seller', lazy="dynamic")


    def __repr__(self):
        return "Name [{}] County [{}] Phone [{}]".format(self.username, self.county, self.phone_number)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_sec=3600):
        return jwt.encode({'user_id': self.id, 'expire_time': time() + expires_sec}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def check_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except:
            return None
        return Users.query.get(user_id)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checked = db.Column(db.Boolean, default=False)
    buyer_name = db.Column(db.String(50), db.ForeignKey("users.username"))
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    def __repr__(self):
        return "{} placed an order to {}".format(self.purchaser.username, self.seller.username)#Debugging purposes


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    sender = db.relationship("Users", foreign_keys=[sender_id])
    receiver = db.relationship("Users", foreign_keys=[receiver_id])


@login.user_loader
def Load_user(id):
    return Users.query.get(int(id))
