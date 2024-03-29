from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = "ab6ad1c5-dce7-4109-81d5-a02b625ca46d"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'brianoyaro2000@gmail.com'
app.config['MAIL_PASSWORD'] = 'ewxp kgic evyf lwmg'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
mail = Mail(app)
login.login_view = 'login'

from app import routes, models, error
