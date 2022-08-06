
from jsonschema import ValidationError
import os
import joblib
from src.get_data import read_params
from src.prediction_validation import inp_dict_validator
import numpy as np
import pickle
import pandas as pd

config_path = 'params.yaml'


def Predict(data):
    try:
        config = read_params(config_path)
        model_foldername = config['model']['model_foldername']
        model_name = config['model']['model_name']

        model_path = os.path.join(model_foldername,model_name)

        model = joblib.load(model_path)

        prediction = model.predict(data)

        thyroid_condition_dict = dict()
        thyroid_condition_dict['A'] = 'hyperthyroid'
        thyroid_condition_dict['B'] = 'T3 toxic'
        thyroid_condition_dict['C'] = 'toxic goitre'
        thyroid_condition_dict['D'] = 'secondary toxic'
        thyroid_condition_dict['E'] = 'hypothyroid'
        thyroid_condition_dict['F'] = 'primary hypothyroid'
        thyroid_condition_dict['G'] = 'compensated hypothyroid'
        thyroid_condition_dict['H'] = 'secondary hypothyroid'
        thyroid_condition_dict['I'] = 'increased binding protein'
        thyroid_condition_dict['J'] = 'decreased binding protein'
        thyroid_condition_dict['K'] = 'concurrent non-thyroidal illness'
        thyroid_condition_dict['L'] = 'consistent with replacement therapy'
        thyroid_condition_dict['M'] = 'underreplaced'
        thyroid_condition_dict['N'] = 'overreplaced'
        thyroid_condition_dict['O'] = 'antithyroid drugs'
        thyroid_condition_dict['P'] = 'I131 treatment'
        thyroid_condition_dict['Q'] = 'surgery'
        thyroid_condition_dict['R'] = 'discordant assay results'
        thyroid_condition_dict['S'] = 'elevated TBG'
        thyroid_condition_dict['T'] = 'elevated thyroid hormones'
        thyroid_condition_dict['Others'] = 'no condition requiring comment'

        print(thyroid_condition_dict)

        prediction = thyroid_condition_dict[prediction[0]]

        return prediction
    
    except Exception as e:
        print(f"Error occured in Predict function.")
        raise e

def form_response(dict_request):

    try:
        validated_inputs = inp_dict_validator(**dict_request)
        input_dict = validated_inputs.dict()
        print(input_dict)

        data = pd.DataFrame(input_dict,index=[0])
        print(data)

        config = read_params(config_path)
        preprocess_pipe_foldername = config['preprocess']['preprocess_pipe_foldername']
        preprocess_pipe_filename = config['preprocess']['preprocess_pipe_filename']
        preprocess_pipe_path = os.path.join(preprocess_pipe_foldername, preprocess_pipe_filename)

        with open(preprocess_pipe_path,'rb') as preprocess_file:
            preprocess_pipe = pickle.load(preprocess_file)
        
        transformed_data = preprocess_pipe.transform(data)
        print(transformed_data)

        response = Predict(transformed_data)
        return response
        
    except ValidationError as e:
        print(f"Validation error: {str(e)}")
        raise e
        




