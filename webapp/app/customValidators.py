# Throw error
from wtforms.validators import ValidationError
# Database access
from app.models import User
# Encryption
from passlib.hash import pbkdf2_sha256

# Used to find if username is available
def uname_avail(form, field):
    username_entered = field.data
    
    user_obj = User.query.filter_by(username = username_entered).first()
    if user_obj is not None:
        raise ValidationError("Username taken")

# Determines if username is in db
def uname_valid(form, field):
    username_entered = form.username.data

    # Checks if username exists
    user_obj = User.query.filter_by(username = username_entered).first()
    if user_obj is None:
        raise ValidationError("Username incorrect")

# Determines if password matches stored user password
def pwd_valid(form, field):
    username_entered = form.username.data
    password_entered = field.data
    
    user_obj = User.query.filter_by(username = username_entered).first()

    if user_obj is not None:
        # Checks if password entered matches database password
        if not pbkdf2_sha256.verify(password_entered, user_obj.password):
            raise ValidationError("Password incorrect")