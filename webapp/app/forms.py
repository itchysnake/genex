# Creation of FlaskForm
from flask_wtf import FlaskForm
# Fields for FlaskForm
from wtforms import (StringField, IntegerField, DecimalField, PasswordField, 
                     BooleanField, SubmitField, RadioField)
# Validators
from wtforms.validators import (InputRequired, Length, EqualTo, NumberRange, ValidationError, Required)
from app.customValidators import (uname_avail, uname_valid, pwd_valid, token_name_avail,
                                  token_sym_avail, email_valid)

class RegisterForm(FlaskForm):
    email = StringField(label = "Email",
                       validators = [InputRequired("Email Required"),
                                     email_valid],
                       render_kw={"placeholder": "email"})
    
    username = StringField(label = "Username",
                           validators = [InputRequired("Username required"),
                                         Length(min = 4, message = "Longer than 4 chars"),
                                         uname_avail],
                           render_kw={"placeholder": "username"})
    
    password = PasswordField(label = "Password",
                             validators = [InputRequired("Password required"),
                                         Length(min = 4, message = "Longer than 4 chars")],
                             render_kw={"placeholder": "password"})
    
    confirm_pwd = PasswordField(label = "Repeat Password",
                                validators = [InputRequired("Password required"),
                                              EqualTo("password","Passwords must match")],
                                render_kw={"placeholder": "confirm password"})
    
    submit = SubmitField("Register")
    
class LoginForm(FlaskForm):
    username = StringField(label = "Username",
                           validators = [InputRequired("Username required"),
                                         uname_valid],
                           render_kw={"placeholder": "username"})
    
    password = PasswordField(label = "Password",
                             validators = [InputRequired("Password required"),
                                           pwd_valid],
                             render_kw={"placeholder": "password"})
    
    submit = SubmitField("Login")
    
class IssuerForm(FlaskForm):
    token_name = StringField(label = "Token Name",
                             validators = [InputRequired("Token name required"),
                             Length(min=4, max=25, message="Between 4 and 25 characters"),
                             token_name_avail])
    
    token_symbol = StringField(label = "Token Symbol",
                               validators = [InputRequired("Token symbol required"),
                               Length(min=1, max=5, message= "Between 1 and 4 characters"),
                               token_sym_avail])
    
    total_supply = IntegerField(label = "Total Supply",
                                validators = [InputRequired("Total supply required"),
                                              NumberRange(min = 1, max = None, message = "Minimum 1")])
    
    submit = SubmitField("Issue")
    
class TokenOrder(FlaskForm):
    price = DecimalField(label = "Price",
                         places=2,
                         validators = [InputRequired("Quantity required")])
    
    type = RadioField(label = "Type",
                          validators = [InputRequired()],
                          choices = [("bid", "Bid"),
                                     ("offer","Offer")],
                          default = "bid")
    
    quantity = IntegerField(label = "Quantity",
                            validators = [InputRequired("Quantity required"),
                                          NumberRange(min = 1, max = None, message = "Minimum 1")])
    
    submit = SubmitField("Order")
    