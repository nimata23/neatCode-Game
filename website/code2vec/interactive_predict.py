import traceback

from .common import common
from .extractor import Extractor
import os.path
from os import path

SHOW_TOP_CONTEXTS = 10
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = 'website/code2vec/JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'


class InteractivePredictor:
    exit_keywords = ['exit', 'quit', 'q']

    def __init__(self, config, model):
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = Extractor(config,
                                        jar_path=JAR_PATH,
                                        max_path_length=MAX_PATH_LENGTH,
                                        max_path_width=MAX_PATH_WIDTH)

    def read_file(self, input_filename):
        with open(input_filename, 'r') as file:
            return file.readlines()

    def predict(self):
        ''' print('test jar file path')
        if path.exists(JAR_PATH):
            print('jar exists')
        else:
            print('error with jar path')
        '''
        #takes a the input_file name as a parameter, makes it easier to create a database of files with similar names to use
        input_filename = 'website/code2vec/Input.java'

        '''#check the file path
        if path.exists(input_filename):
            print('file exists')
        else:
            print('error with file path')
        '''
        top_names = []
        #print('Starting interactive prediction...')
        #removed code for user input, we only want to run a prediction on the file
        try:
            predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(input_filename)
        except ValueError as e:
            print(e)
        raw_prediction_results = self.model.predict(predict_lines)
        method_prediction_results = common.parse_prediction_results(
        raw_prediction_results, hash_to_string_dict,
            self.model.vocabs.target_vocab.special_words, topk=SHOW_TOP_CONTEXTS)
        for raw_prediction, method_prediction in zip(raw_prediction_results, method_prediction_results):
            print('Original name:\t' + method_prediction.original_name)
            for name_prob_pair in method_prediction.predictions:
                print('\t(%f) predicted: %s' % (name_prob_pair['probability'], name_prob_pair['name']))
                top_names.append(name_prob_pair)
            print('Attention:')
            for attention_obj in method_prediction.attention_paths:
                print('%f\tcontext: %s,%s,%s' % (
                attention_obj['score'], attention_obj['token1'], attention_obj['path'], attention_obj['token2']))
            if self.config.EXPORT_CODE_VECTORS:
                print('Code vector:')
                print(' '.join(map(str, raw_prediction.code_vector)))
        return top_names
