from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import User
from flask_login import login_required, current_user, login_user, logout_user
import re
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

# logs in user if user exists, username and password are correct
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    #print('in the login method')
    if request.method == 'POST':
        print('method is post')
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
        user = User.query.filter_by(username = username).first()
        print(user)
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember = True)
                return redirect(url_for('views.game', user=current_user,code=None, active_page='game.html'))
            else:
                flash("Password is incorrect")
        else:
            flash("User does not exist")
    
    return render_template("login.html", user=current_user, active_page='login')


#logs out the user and returns to login page
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



#creates a new user if the requirements are met
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    #pull infro from request form
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #search for username
        user = User.query.filter_by(username=username).first()
        regexp = re.compile('[^0-9za-zA-Z]+')
        #if there is already a user w/ this username, alert the user to choose
        # a differet name.
        if user:
            return "This username is already taken"

        #check password validity
        #do the passwords match
        elif password1 != password2:
            return "Passwords must match"
        #is the password longer than 6 chars
        elif len(password1) < 7:
            return "Password must be at least 7 chatacter long"
        #does the password include a captial letter
        elif password1.islower():
            return 'Password must contain at least 1 captial letter'
        #does the password include a numner or special character
        elif not re.search('[0-9]', password1) and not regexp.search(password):
            return 'Password must contain at least 1 number or special character'
        else: # if all tests pass then create the user
            new_user = User(username=username, password=password1)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.home'))
    
    return render_template('signup.html', user-current_user, active_page = 'signup')




        