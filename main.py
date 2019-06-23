from flask import Flask, request, redirect, render_template
import cgi
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("signup.html", title = "User Signup")

@app.route("/", methods=["POST"])
def validate_input():
    # Collect user inputs:
    username = request.form['username']
    password = request.form['password']
    pwd_chk = request.form['ck_password']
    email = request.form['email']

    # Set up falsy user error variables:
    username_error = ""
    password_error = ""
    pwd_match_error = ""
    email_error = ""

    # Validate username and clear value if invalid:
    if not 3 <= len(username) <= 20:
        username_error = "Your username must be between 3 and 20 characters."
        username = ""
    elif " " in username:
        username_error = "Your username must not contain a space."
        username = ""

    # Validate password:
    if not 3 <= len(password) <= 20:
        password_error = "Your password must be between 3 and 20 characters."
    elif " " in password:
        password_error = "Your password must not contain a space."
    
    # Validate passwords match:
    if not password == pwd_chk:
        pwd_match_error = "Your passwords did not match, please type carefully!"
    
    # Validate email:
    if email:
        # Check for spaces in email address
        if " " in email: 
            email_error = "The email address cannot contain spaces."
            email = ""
        
        # Check for valid email formatting
        is_valid_email = re.match("[^@]+@[^@]+\.[^@]+", email)
        if not is_valid_email:
            email_error = "The email address you entered is not a valid email."
            email = ""
        
    # If no errors are present, render welcome, else redisplay form w/ errors
    if not username_error and not password_error and not pwd_match_error and not email_error:
        return render_template('welcome.html', title = "Welcome!", username = username)
    else:
        return render_template('signup.html', title = "User Signup", username_error = username_error, password_error = password_error, pwd_match_error = pwd_match_error, email_error = email_error, username = username, email = email)
        
app.run()