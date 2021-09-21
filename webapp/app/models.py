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
    
    # one-to-one > User.token.<col>
    token = db.relationship("Token", backref="user", lazy=True, uselist=False)
    # one-to-many > User.orders.<col>
    order = db.relationship("Order", backref="user")
    # one-to-many > User.trades.<col>
    trade = db.relationship("Trade", backref="user")
    
class Token(db.Model):
    """
    Tokens table
    """
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    name = db.Column(db.String(), unique = True, nullable = False)
    symbol = db.Column(db.String(), unique = True, nullable = False)
    total_supply = db.Column(db.Integer(), nullable = False)

    # one-to-many > Token.orders.<col>
    order = db.relationship("Order", backref="token", cascade = "all,delete")
    # one-to-many > Token.trades.<col>
    trade = db.relationship("Trade", backref="token")
    
class Order(db.Model):
    """
    Orders table
    """
    __tablename__ = "orders"
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    token_id = db.Column(db.Integer, db.ForeignKey("tokens.id"), nullable = False)
    type = db.Column(db.String(), nullable = False)
    price = db.Column(db.Float(4), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    filled = db.Column(db.Boolean, default=False)
    amount_filled = db.Column(db.Integer)
    
class Trade(db.Model):
    """
    Trades table
    """
    __tablename__ = "trades"
    
    id = db.Column(db.Integer, primary_key = True)
    bid_order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable = False)
    offer_order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable = False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    token_id = db.Column(db.Integer, db.ForeignKey("tokens.id"), nullable = False)
    price = db.Column(db.Float(4), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    
    # one-to-many > Trade.orders.<col>
    order = db.relationship("Order", backref="trade", cascade = "all,delete")