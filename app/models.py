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
    type = db.Column(db.String(1))
    orderee = db.relationship("Order", foreign_keys='Order.buyer_name', backref='purchaser', lazy="dynamic")
    ordered_to = db.relationship("Order", foreign_keys='Order.seller_id', backref='seller', lazy="dynamic")

    def __repr__(self):
        return "Name [{}] County [{}] Phone [{}]".format(self.username, self.county, self.phone_number)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_name = db.Column(db.String(50), db.ForeignKey("users.username"))
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    def __repr__(self):
        return "{} placed an order to {}".format(self.purchaser.username, self.seller.username)#Debugging purposes


@login.user_loader
def Load_user(id):
    return Users.query.get(int(id))
