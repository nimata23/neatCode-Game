#required imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from flask_login import login_required, current_user
from .code2vec import interactive_predict
import os
from gensim.models import KeyedVectors as word2vec
from . import target_model, predictor
import re


views = Blueprint('views', __name__)
lives_left = 3
best_score = 0

#home page
@views.route('/', methods=['GET','POST'])
def home():

    return render_template("home.html", user=current_user, active_page='home')

#leaderbaord page
@views.route('/leaderboard', methods=['GET','POST'])
def leaderbaord():

    return render_template("leaderboard.html", user=current_user, active_page='home')

#game page
@views.route('/game/<level><fileNum>', methods=['GET','POST'])
@login_required
def game(level, fileNum):
    global predictor, lives_left, best_score
    
    current_score = current_user.current_score

    #as default select the first file of the chosen level"
    base_path = "website/code2vec/java_samples/" + level + '/file'
    filename = base_path + str(fileNum) +'.java'
    print(os.path.exists(filename))
    code_block = read_file(filename)

    #file max, this is the number of sample file in EACH LEVEL! 
    #it is assumed ALL LEVEL have the SAME number of samples
    file_max = 2

    #similarity score
    sim_score = 0.0

    #print to test
    for line in code_block:
        print(line)
    

    #see if there is a next file, change value accordingly
    if int(fileNum) < file_max:
        next_file = str(int(fileNum) + 1)
    else:
        next_file = '0'



    if request.method == 'POST':
        #print('lives left: ' + str(lives_left))
        predict = request.form.get('answer')
        print('predict value: ' + predict)
        
            
        if lives_left >=1:
            #if there is prediction, create the predictor and pass in the file you are predicting 
            #the name of
            print("calling predict")

            #overwrite the input file
            overwrite(code_block)

            #call predict and get the list of top name-probability pairs
            top_names = predictor.predict()

            #tokenize the method name pass by the user
            if len(top_names)> 0:
                
                try:
                    tokens = tokenize(predict)
                    tokens = format(tokens)
                    similarity_score = test_similarity(top_names, tokens)
                except:
                    flash('We do not recognize some of the words in your answer.')
                    similarity_score = "0"
                
                sim_score = re.sub(r"[\([{})\]]", "", similarity_score)

                if float(sim_score) > best_score:
                    best_score = float(sim_score)

            if lives_left == 1:
                if best_score < 0:
                    points = 0
                else:
                    points = int(best_score * 100.0)
                current_user.current_score = current_score + points
                db.session.commit()
            lives_left = lives_left - 1     
                
        else:
            flash('you are out of lives, please move to the next example.')
            lives_left = 3
    

    return render_template("game.html", user=current_user, code=code_block, similarity = sim_score,
        curr_level=level, next_file=str(next_file), lives = lives_left,active_page='game.html')
    

@views.route('/levelselect',  methods=['GET','POST'])
@login_required
def levelselect():
    '''if request.method == 'POST':
        level1 = request.form.get('level1')
        level2 = request.form.get('level2')
        level3 = request.form.get('level3')

        if level1 == True:
            redirect(url_for('views.game', level='level1'))
        elif level2 == True:
            redirect(url_for('views.game', level='level2'))
        elif
            redirect(url_for('views.game', level='level3'))
        else:
            flash('please select a level')
    '''    
    return render_template("levelselect.html", user= current_user, active_page='levelselect.html')



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


def test_similarity(top_names, tokens):
    global target_model

    #get the top answer from code2vec
    top_pair = top_names[0]
    top_pair = format(top_pair['name'])
    
    similarity = str(target_model.similarity(top_pair, tokens))
    
    return similarity

def tokenize(predict):
    predict = predict.lower()
    tokens = predict.split('_')             
    return tokens


#formats with '|' between words, needed for code2vec similarity
def format(tokens):
    method_name = ''

    for i in range(len(tokens)):
        if i == (len(tokens) - 1):
            method_name = method_name + tokens[i]
        else:
            method_name = method_name + tokens[i] + '|'

    return method_name

