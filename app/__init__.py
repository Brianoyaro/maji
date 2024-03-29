from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
login.login_view = 'auth.login'

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app import models
    from app.error import bp as error_bp
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp

    app.register_blueprint(error_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    return app
