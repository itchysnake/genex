from flask import Flask, render_template, redirect, url_for

# import all forms
from forms import RegistrationForm, LoginForm

# databse
from models import User
from flask_sqlalchemy import SQLAlchemy

# Configure app
app = Flask(__name__)
app.secret_key = "password"

# Configure db
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vevrmxjgsdtlac:751dd9301bc9599bbbd483b5a9dc72d3dc027fce70d7d37382b29625c4cf43b6@ec2-54-220-14-54.eu-west-1.compute.amazonaws.com:5432/dbbn7lbgl3cn00"
db = SQLAlchemy(app)

@app.route("/", methods = ["GET","POST"])
def index():
    
    # Update DB if registration succesful
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        
        # add to DB
        user = User(username = username,
                    password = password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("login"))
    
    return render_template("index.html", form = reg_form)

@app.route("/login", methods = ["GET", "POST"])
def login():

    # Allow login if succesful    
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return "Logged in!"

    return render_template("login.html", form = login_form)

if __name__ == "__main__":
    app.run(debug = True)