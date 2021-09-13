from flask import Flask, render_template

# import all forms
from forms import *

# App configuration
app = Flask(__name__)
app.secret_key = "password"

@app.route("/", methods = ["GET","POST"])
def index():
    
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        return "Horray!"
    
    return render_template("index.html", form = registration_form)

if __name__ == "__main__":
    app.run(debug = True)