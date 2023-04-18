#required imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from flask_login import login_required, current_user
from .code2vec import code2vec, interactive_predict
import random
import os


views = Blueprint('views', __name__)


#home page
@views.route('/', methods=['GET','POST'])
def home():

    return render_template("home.html", user=current_user, active_page='home')

#leaderbaord page
@views.route('/leaderboard', methods=['GET','POST'])
def leaderbaord():

    return render_template("leaderboard.html", user=current_user, active_page='home')

#game page
@views.route('/game', methods=['GET','POST'])
@login_required
def game():
    #as soon as page loads, load the code2vec model, get the model and config values
    model, config = code2vec.c2v()

    #as default select the first file of the first level
    base_path = "website/code2vec/java_samples/"
    file_base = base_path + 'level1/file'
    file_num = 1
    filename = file_base + str(file_num) +'.java'
    code_block = read_file(filename)

    #print to test
    for line in code_block:
        print(line)
    #3 attempts to answer correctly
    lives_left = 3

    if request.method == 'POST':
        #get input from forms (level selection, name predition, or move to next example)
        level_select = request.form.get('level')
        next_file = request.form.get('next')
        predict = request.form.get('answer')
        print('predict value: ' + predict)
        #if changing the level, change the base of the file names and update the displayed information
        if level_select:
            file_num=1
            if level_select == 1:
                file_base = base_path + "level1/file"
                filename = file_base + '1.java'
                code_block = read_file(filename1)
            elif level_select == 2:
                file_base = base_path + "level2/file"
                filename = file_base + '1.java'
                code_block = read_file(filename)
            elif level_select == 3:
                file_base = base_path + "level3/file"
                filename = file_base + '1.java'
                code_block = read_file(filename)
        
        #check if you are moving to the next example
        elif next_file:
            #picks a random file from the same level  -- EDIT HERE TO CHANGE NUMBER OF JAVA EXAMPLES!
            file_num = file_num +1
            #add the number to the filename and read the file
            filename = filebase + str(file_num) +".java"
            code_block = read_file(filepath)

        #check if you are predicting the method name
        elif predict != "":
            #if there is prediction, create the predictor and pass in the file you are predicting 
            #the name of
            print("calling predict")
            #overwrite the input file
            overwrite(code_block)

            #call predict
            predictor = interactive_predict.InteractivePredictor(config, model)
            predictor.predict()
            #lives_left  = lives_left - 1
    
        #if the user is out of lives
        elif predict and lives <= 0:
            flash("no lives left, please click next")
    return render_template("game.html", user=current_user, code=code_block, active_page='game.html')

def overwrite(code_block):
    #open the input file that predict uses 
    write_file = open("website/code2vec/Input.java", 'w')

    #for every line in the code block [from sample code snippets] write to input file
    for line in code_block:
        write_file.write(line)
    write_file.close()

def read_file(filepath):
    file1 = open(filepath, 'r')
    data = file1.readlines()
    file1.close()
    return data

