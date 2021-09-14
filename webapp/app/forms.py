# Creation of FlaskForm
from flask_wtf import FlaskForm
# Fields for FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField)
# Validators
from wtforms.validators import (InputRequired, Length, EqualTo, ValidationError)
from app.customValidators import (uname_avail, uname_valid, pwd_valid)

class RegisterForm(FlaskForm):
    username = StringField(label = "username",
                           validators = [InputRequired("Username required"),
                                         Length(min = 4, message = "Longer than 4 chars"),
                                         uname_avail])
    
    password = PasswordField(label = "password",
                             validators = [InputRequired("Password required"),
                                         Length(min = 4, message = "Longer than 4 chars")])
    
    confirm_pwd = PasswordField(label = "password",
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