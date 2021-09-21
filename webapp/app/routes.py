# App dependancies
from app import app, forms
from app.models import db, User, Token, Order
# Flask-general
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
# Password encryption
from passlib.hash import pbkdf2_sha256

# HOME
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("index.html")

# DISCOVER
@app.route("/discover", methods=["GET"])
@login_required
def discover():

    tokens = Token.query.all()
    
    return render_template("discover.html", tokens = tokens)

# TOKEN PAGE
@app.route("/token/<token_id>", methods = ["GET","POST"])
@login_required
def token(token_id):
    
    # pull token information from url request
    token = Token.query.filter_by(id = token_id).first()
    
    # order form
    order_form = forms.TokenOrder()
    
    if order_form.validate_on_submit():
        
        # add to db
        type = order_form.type.data
        price = order_form.price.data
        quantity = order_form.quantity.data
        
        order = Order(user_id = current_user.id,
                      token_id = token_id,
                      type = type,
                      price = price,
                      quantity = quantity)
        
        db.session.add(order)
        db.session.commit()
        
        # Flash feedback
        flash("Order placed")
        return redirect(url_for("index"))
    
    return render_template("token.html",
                           token = token,
                           order_form = order_form)

# PORTFOLIO
@app.route("/portfolio", methods = ["GET"])
@login_required
def portfolio():
    
    # Pull all current user orders
    orders = Order.query.filter_by(user_id = current_user.id).all()
    
    return render_template("portfolio.html",
                           orders = orders)

# ISSUER CONTROLS
@app.route("/issuer", methods=["GET","POST"])
@login_required
def issuer():
    
    # if issuer has a token redirect to issuer/asset
    if current_user.token is not None:
        flash("You already have a token!")
        return redirect(url_for("index"))
    
    # issue token form
    issuer_form = forms.IssuerForm()
        
    if issuer_form.validate_on_submit():

        # add to DB
        token_name = issuer_form.token_name.data
        token_symbol = issuer_form.token_symbol.data
        total_supply = issuer_form.total_supply.data
        
        token = Token(name = token_name,
                      user_id = current_user.id,
                      symbol = token_symbol,
                      total_supply = total_supply)
        
        
        db.session.add(token)
        db.session.commit()
        
        # Flash feedback
        flash("Succesfully issued token.", category="success")
        
        return redirect(url_for("index"))
    
    return render_template("issuer.html", form = issuer_form)

# AUTHORISATION
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
        flash("Succesfully registered.", category="success")
        
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
        flash("Succesfully logged in.", category="success")
        
        return redirect(url_for("index"))
    
    return render_template("login.html", form=login_form)   

@app.route("/logout", methods = ["GET"])
@login_required
def logout():
     logout_user()
     flash("Succesfully logged out.", category = "success")
     return redirect(url_for("index"))