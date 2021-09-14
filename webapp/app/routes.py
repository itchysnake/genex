# App dependancies
from app import app, forms
from app.models import User, db
# Flask-general
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
# Password encryption
from passlib.hash import pbkdf2_sha256

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    
    # Instantiate form
    reg_form = forms.RegisterForm()
    
    # Redirect to login upon registration
    if reg_form.validate_on_submit():
        
        # Prep data for DB
        username = reg_form.username.data        
        hashed_pwd = pbkdf2_sha256.hash(reg_form.password.data)
        
        # Save to DB
        user = User(username = username,
                    password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        
        # Flash feedback
        flash("Succesfully registered, please login.", category="success")
        
        return redirect(url_for("login"))
    
    return render_template("register.html", form=reg_form)

@app.route("/login", methods=["GET","POST"])
def login():
    
    # Instantiate form
    login_form = forms.LoginForm()
    
    # Redirect to index upon login
    if login_form.validate_on_submit():
    
        # Log user in
        username_entered = login_form.username.data
        user_obj = User.query.filter_by(username = username_entered).first()
        login_user(user_obj)
        
        # Flash feedback
        flash("Succesfully registered, please login.", category="success")
        
        return redirect(url_for("index"))
    
    return render_template("login.html", form=login_form)   

@app.route("/logout", methods = ["GET"])
@login_required
def logout():
     logout_user()
     flash("Log out succesful.", category = "success")
     return redirect(url_for("index"))