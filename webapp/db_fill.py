from config import Config
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# Database
from app.models import db, User, Token, Order, Trade, Ownership

# Initialise app
app = Flask(__name__)

# Gives access to required keys
app.config.from_object(Config)

# Configure DB
db = SQLAlchemy(app)

def create_users():
    
    user1 = User("bailey", "password", "bailey@gmail.com")
    user2 = User("pedro","password","pedro@gmail.com")
    
    db.session.add(user1)
    db.session.add(user2)
    
    db.session.commit()
    
def create_tokens():
    token1 = Token(1,"Bailey Token","BDVT",10000, "Developer","Nerd")
    token2 = Token(2,"Pedro Token","PDST",1000, "Comedian","Crack Addict")
    
    db.session.add(token1)
    db.session.add(token2)
    
    db.session.commit()

def test_orders():
    # Bailey's Token Spread
    # 1 Trade of 15 for $10
    # 1 order outstanding of 10 offers (sell pressure)
    order1 = Order(1,1,"offer",10,25)
    order2 = Order(2,1,"bid",11,15)
    order3 = Order(2,1,"bid",10,5)
    
    # Pedro's Token Spread
    # No trades but 50/50 and buying pressure
    order3 = Order(2,2,"offer",15,35)
    order4 = Order(1, 2, "bid",13, 40)
    
    db.session.add(order1)
    db.session.add(order2)
    db.session.add(order3)
    db.session.add(order4)
    db.session.commit()

# Create tables
def main():
    with app.app_context():
        create_users()
        create_tokens()
        test_orders()

# Run main() then closes app
if __name__=="__main__":
    main()