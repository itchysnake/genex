from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    # Fields
    username = StringField(label = "username",
                           validators=[InputRequired(message="Username required"),
                                       Length(min=4, max=25, message = "Between 4 and 25")])
    
    password = PasswordField(label = "password",
                           validators=[InputRequired(message="Password required"),
                                       Length(min=4, max=25, message = "Between 4 and 25")])

    confirm_pwd = PasswordField(label = "confirm_pwd",
                           validators=[InputRequired(message="Username required"),
                           EqualTo("password", message = "Passwords must match")])
    
    submit_button = SubmitField("Create")
    
    