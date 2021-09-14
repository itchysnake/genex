# only run once

from flask import Flask
from app.models import db
from config import Config

# Initialise app
app = Flask(__name__)
# Gives access to required keys
app.config.from_object(Config)

db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()