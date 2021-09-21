# only run once

from flask import Flask
from app.models import db
from config import Config

# Initialise app
app = Flask(__name__)

# Gives access to required keys
app.config.from_object(Config)

# Initialise database
db.init_app(app)

# Create tables
def main():
    with app.app_context():
        db.create_all()

# Run main() then closes app
if __name__=="__main__":
    main()