
from jsonschema import ValidationError
import os
import joblib
from src.get_data import read_params
from src.prediction_validation import inp_dict_validator
import numpy as np
import pickle

config_path = 'params.yaml'


def Predict(data):
    try:
        config = read_params(config_path)
        model_foldername = config['model']['model_foldername']
        model_name = config['model']['model_name']

        model_path = os.path.join(model_foldername,model_name)

        model = joblib.load(model_path)

        prediction = model.predict(data).to_list()[0]
        return prediction
    
    except Exception as e:
        print(f"Error occured in Predict function.")
        raise e

def form_response(dict_request):

    try:
        # since we will get the numerial values in the form of strings from
        # the html form, we first need to convert their data type from string to float
        for feature in ['age','TSH','T3','TT4','T4U','FTI','TBG']:
            dict_request[feature] = float(dict_request[feature])

        inp_dict_validator(**dict_request)

        data = dict_request.values()
        data = np.array(list(data))

        config = read_params(config_path)
        preprocess_pipe_foldername = config['preprocess']['preprocess_pipe_foldername']
        preprocess_pipe_filename = config['preprocess']['preprocess_pipe_filename']
        preprocess_pipe_path = os.path.join(preprocess_pipe_foldername, preprocess_pipe_filename)

        with open(preprocess_pipe_path,'rb') as preprocess_file:
            preprocess_pipe = pickle.load(preprocess_file)

        transformed_data = preprocess_pipe.transform(data)

        response = Predict(transformed_data)
        return response
        
    except ValidationError as e:
        print(f"Validation error: {str(e)}")
        raise e
        




