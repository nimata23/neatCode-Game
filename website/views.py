#required imports
from flask import Vlueprint, render_template, request, redirect, url_for, flash
from . import db
from flask_login import login_required, current_user


view = Blueprint('views', __name__)

#home page
@view.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        #this is be where we call code2vec to see if what they typed is correct
        print('do something')

    return render_template("home.html", user=current_user, active_page='home')






