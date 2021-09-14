# File that creates the app
# All imports for the app itself should be to this file

# App initialisation
from flask import Flask
# Configuration
from config import Config
# Database initialisation
from flask_sqlalchemy import SQLAlchemy
from app.models import User
# Login manager initialisatoin
from flask_login import LoginManager

# Initialise app
app = Flask(__name__)
app.config.from_object(Config)

# Configure DB
db = SQLAlchemy(app)

# Configure login & session manager
login = LoginManager(app)
login.init_app(app)

# Sets login redirect for @login_required
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))