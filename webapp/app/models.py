from flask_sqlalchemy import SQLAlchemy
# Manages user session
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    Users table
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(), unique=True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    
    # one-to-one > User.token.<column>
    token = db.relationship("Token", backref="user", lazy=True, uselist=False)
    
class Token(db.Model):
    """
    Tokens table
    """
    __tablename__ = "tokens"
    id = db.Column(db.Integer, primary_key = True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    
    name = db.Column(db.String(), unique = True, nullable = False)
    symbol = db.Column(db.String(), unique = True, nullable = False)
    totalSupply = db.Column(db.Integer(), nullable = False)
    
    # remains many-to-one > Token.user
    # can't map a class twice for some reason (e.g. User.token & Token.user)
    #user = db.relationship("User", backref="token", lazy=True)