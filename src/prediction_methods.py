
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
        validated_inputs = inp_dict_validator(**dict_request)
        input_dict = validated_inputs.dict()

        data = input_dict.values()
        data = np.array(list(data))
        print(data)

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
        




