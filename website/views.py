#required imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from flask_login import login_required, current_user
#from code2vec import code2vec -- import from subdirectory

views = Blueprint('views', __name__)
code2vec_model = /code2vec/models/java14_model/saved_model_iter8.release


#home page
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    #as soon as page loads, load the code2vec model, I think below is how it would work
    #code2vec("--load"= code2vec_model, "--predict")
    if request.method == 'POST':
        #edit the input.java message (my idea is to write & rewrite the file
        # and the use input.java as the source to display the code too?)

        #this is be where we call code2vec to see if what they typed is correct
        print('do something')

    

    return render_template("home.html", user=current_user, active_page='home')





