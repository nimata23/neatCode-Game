#required imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from flask_login import login_required, current_user
from .code2vec import code2vec, interactive_predict
import random


views = Blueprint('views', __name__)


#home page
@views.route('/', methods=['GET','POST'])
@login_required
def home():

    return render_template("home.html", user=current_user, active_page='home')


@views.route('/', methods=['GET','POST'])
@login_required
def play_game():
    #as soon as page loads, load the code2vec model, get the model and config values
    model, config = code2vec.c2v()

    #as default select the first file of the first level
    file_base = "website/java_samples/level1/file"
    filename = file_base + '1' + ".java"
    lines = read_file(filename)

    #3 attempts to answer correctly
    lives_left = 3

    if request.method == 'POST':
        #get input from forms (level selection, name predition, or move to next example)
        level_select = request.form.get('level')
        next_file = request.form.get('next')
        predict = request.form.get('prediction')

        #if changing the level, change the base of the file names and update the displayed information
        if level_select:
            if level_select == 1:
                file_base = "java_samples/level1/file"
                filename = file_base + '1' + ".java"
                lines = read_file(filename)
            elif level_select == 2:
                file_base = "java_samples/level2/file"
                filename = file_base + '1'+ ".java"
                lines = read_file(filename)
            elif level_select == 3:
                file_base = "java_samples/level3/file"
                filename = file_base + '1'+ ".java"
                lines = read_file(filename)
        
        #check if you are moving to the next example
        elif next_file:
            #picks a random file from the same level  -- EDIT HERE TO CHANGE NUMBER OF JAVA EXAMPLES!
            num = str(random.randint(2, 10))
            #add the number to the filename and read the file
            filename = filebase + num +".java"
            lines = read_file(filename)

        #check if you are predicting the method name
        elif predict and lives > 0:
            if there is prediction, create the predictor and pass in the file you are predicting 
            the name of
            predictor = InteractivePredictor(config, model)
            predictor.predict(filename)
            lives_left  = lives_left - 1
    
        if the user is out of lives
        elif predict and lives <= 0:
            flash("no lives left, please click next")
    return render_template("home.html", user=current_user, code_lines = lines, active_page='home')

def read_file(filename):
    file1 = open(filename, 'r')
    lines = file1.readlines()
    return lines

