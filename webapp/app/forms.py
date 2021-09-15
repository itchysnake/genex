# Creation of FlaskForm
from flask_wtf import FlaskForm
# Fields for FlaskForm
from wtforms import (StringField, IntegerField, PasswordField, BooleanField, SubmitField)
# Validators
from wtforms.validators import (InputRequired, Length, EqualTo, NumberRange, ValidationError)
from app.customValidators import (uname_avail, uname_valid, pwd_valid, token_name_avail,
                                  token_sym_avail)

class RegisterForm(FlaskForm):
    username = StringField(label = "Username",
                           validators = [InputRequired("Username required"),
                                         Length(min = 4, message = "Longer than 4 chars"),
                                         uname_avail])
    
    password = PasswordField(label = "Password",
                             validators = [InputRequired("Password required"),
                                         Length(min = 4, message = "Longer than 4 chars")])
    
    confirm_pwd = PasswordField(label = "Repeat Password",
                                validators = [InputRequired("Password required"),
                                              EqualTo("password","Passwords must match")])
    
    submit = SubmitField("Register")
    
class LoginForm(FlaskForm):
    username = StringField(label = "Username",
                           validators = [InputRequired("Username required"),
                                         uname_valid])
    
    password = PasswordField(label = "Password",
                             validators = [InputRequired("Password required"),
                                           pwd_valid])
    
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