from flask_sqlalchemy import SQLAlchemy
# Manages user session
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    Users table
    """
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, nullable = False)
    username = db.Column(db.String(), unique=True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    # Add GRAVATAR
    
    # one-to-one > User.token.<col>
    token = db.relationship("Token", backref="user", lazy=True, uselist=False)
    # one-to-many > User.orders.<col>
    order = db.relationship("Order", backref="user")
    # one-to-many > User.trades.<col>
    # trade = db.relationship("Trade", backref="user") <-- DELETE
    # one-to-many > User.ownership
    ownership = db.relationship("Ownership", backref="user")
    
    def __init__(self, username, password):
        self.timestamp = datetime.datetime.utcnow()
        self.username = username
        self.password = password
    
class Token(db.Model):
    """
    Tokens table
    """
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    name = db.Column(db.String(), unique = True, nullable = False)
    symbol = db.Column(db.String(), unique = True, nullable = False)
    total_supply = db.Column(db.Integer(), nullable = False)

    # one-to-many > Token.orders.<col>
    order = db.relationship("Order", backref="token")
    # one-to-many > Token.trades.<col>
    trade = db.relationship("Trade", backref="token")
    # one-to-many > Token.ownership.
    ownership = db.relationship("Ownership", backref="token")
    
    def __init__(self, user_id, name, symbol, total_supply):
        self.timestamp = datetime.datetime.utcnow()
        self.user_id = user_id
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply

    
class Order(db.Model):
    """
    Orders table
    """
    __tablename__ = "orders"
    
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    token_id = db.Column(db.Integer, db.ForeignKey("tokens.id"), nullable = False)
    type = db.Column(db.String(), nullable = False)
    price = db.Column(db.Float(4), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    filled = db.Column(db.Boolean, default=False)
    amount_filled = db.Column(db.Integer)
    
    def __init__(self, user_id, token_id, type, price, quantity, filled = False, amount_filled = 0):
        self.timestamp = datetime.datetime.utcnow()
        self.user_id = user_id
        self.token_id = token_id
        self.type = type
        self.price = price
        self.quantity = quantity
        self.filled = filled
        self.amount_filled = amount_filled 
    
class Trade(db.Model):
    """
    Trades table
    """
    __tablename__ = "trades"
    
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, nullable = False)
    bid_order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable = False)
    offer_order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable = False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    token_id = db.Column(db.Integer, db.ForeignKey("tokens.id"), nullable = False)
    price = db.Column(db.Float(4), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    
    # Allowing multiple foreign keys
    buyer = db.relationship("User", foreign_keys=[buyer_id])
    seller = db.relationship("User", foreign_keys=[seller_id])
    
    # Building the foreign keys
    bid_order = db.relationship("Order", foreign_keys =[bid_order_id])
    offer_order = db.relationship("Order", foreign_keys=[offer_order_id])
    
    def __init__(self, bid_order_id, offer_order_id, buyer_id, seller_id, token_id, price, quantity):
        self.timestamp = datetime.datetime.utcnow()
        self.bid_order_id = bid_order_id
        self.offer_order_id = offer_order_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.token_id = token_id
        self.price = price
        self.quantity = quantity
    
class Ownership(db.Model):
    """
    Tokens owned by user
    """
    __tablename__ = "ownership"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False, primary_key = True)
    token_id = db.Column(db.Integer, db.ForeignKey("tokens.id"), nullable = False)
    quantity = db.Column(db.Integer)