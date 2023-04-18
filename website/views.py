#required imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from flask_login import login_required, current_user
from .code2vec import code2vec, interactive_predict
import os
from gensim.models import KeyedVectors as word2vec


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
    #set users session score to 0
    current_user.current_score = 0

    #as soon as page loads, load the code2vec model, get the model and config values
    model, config = code2vec.c2v()

    #load word2vec model using target name vectors
    vectors_text_path_target = 'website/code2vec/models/java14_model/targets.txt'
    vectors_text_path_tokens = 'website/code2vec/models/java14_model/tokens.txt'
    target_model = word2vec.load_word2vec_format(vectors_text_path_target, binary=False)
    token_model = word2vec.load_word2vec_format(vectors_text_path_tokens, binary=False)
    

    #as default select the first file of the first level
    base_path = "website/code2vec/java_samples/"
    file_base = base_path + 'level1/file'
    file_num = 1
    filename = file_base + str(file_num) +'.java'
    code_block = read_file(filename)

    #file max, this is the number of sample file in EACH LEVEL! 
    #it is assumed ALL LEVEL have the SAME number of samples
    file_max = 2

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
            #add the current similary score [first 2 digits] to current score
            points = int(similarity_score * 100.0)
            current_user.current_score = user.current_score + points

            #picks a random file from the same level  -- EDIT HERE TO CHANGE NUMBER OF JAVA EXAMPLES!
            if file_num < file_max:
                file_num = file_num +1
                #add the number to the filename and read the file
                filename = filebase + str(file_num) +".java"
                code_block = read_file(filepath)
            else:
                flash('You have completed all the exercises in this level.')

        #check if you are predicting the method name
        elif predict != "":
            #if there is prediction, create the predictor and pass in the file you are predicting 
            #the name of
            print("calling predict")
            #overwrite the input file
            overwrite(code_block)

            #call predict and get the list of top name-probability pairs
            predictor = interactive_predict.InteractivePredictor(config, model)
            top_names = predictor.predict()

            #tokenize the method name pass by the user
            if top_names:
                tokens = tokenize(predict)

                #pass required things to similarity test
                similarity_score = test_similarity(top_names, tokens, target_model, token_model)
                print("similarity score: " + str(similarity_score))
                #lives_left  = lives_left - 1
    
        #if the user is out of lives
        elif predict and lives <= 0:
            flash("no lives left, please click next")
    return render_template("game.html", user=current_user, code=code_block, similariy = similarity_score, active_page='game.html')

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


def test_similarity(top_names, tokens, target_model, token_model):
    #get the top answer from code2vec
    top_pair = top_names[0]
    

    #most similar based on the tokens from the name passed in by the user
    from_user = target_model.most_similar(positive=tokens)
    user_top = from_user[0]
    print('from user: ')
    print(from_user)
    similarity = str(target_model.similarity(top_pair['name'], user_top[0]))
    return similarity

def tokenize(predict):
    predict = predict.lower()
    tokens = predict.split('_')
    return tokens
