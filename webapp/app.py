# general
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

# import all forms
from forms import RegistrationForm, LoginForm

# databse
from models import User
from flask_sqlalchemy import SQLAlchemy

# encryption
from passlib.hash import pbkdf2_sha256

# Configure app
app = Flask(__name__)
app.secret_key = "password"

# Configure flask login
login = LoginManager(app)
login.init_app(app)

# Configure db
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vevrmxjgsdtlac:751dd9301bc9599bbbd483b5a9dc72d3dc027fce70d7d37382b29625c4cf43b6@ec2-54-220-14-54.eu-west-1.compute.amazonaws.com:5432/dbbn7lbgl3cn00"
db = SQLAlchemy(app)

# Session loader
@login.user_loader
def load_user(id):
    
    # id must be an int
    return User.query.get(int(id))

@app.route("/", methods = ["GET","POST"])
def index():
    
    # Update DB if registration succesful
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        
        username = reg_form.username.data
        password = reg_form.password.data
        
        hashed_pwd = pbkdf2_sha256.hash(password)
        
        # add to DB
        user = User(username = username,
                    password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("login"))
    
    return render_template("index.html", form = reg_form)

@app.route("/chat", methods = ["GET","POST"])
@login_required
def chat():
    return "Hello"

@app.route("/login", methods = ["GET", "POST"])
def login():

    # Instantiate form
    login_form = LoginForm()
    
    # Login if succesful
    if login_form.validate_on_submit():

        # Log in user        
        username_entered = login_form.username.data
        user_obj = User.query.filter_by(username = username_entered).first()
        login_user(user_obj)
        
        if current_user.is_authenticated:
            return "Logged in with Flask"
        
        return "Login failed"

    return render_template("login.html", form = login_form)

@app.route("/logout", methods = ["GET"])
def logout():
     logout_user()
     return "Logged Out"

if __name__ == "__main__":
    app.run(debug = True)