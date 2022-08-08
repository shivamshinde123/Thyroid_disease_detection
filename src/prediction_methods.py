
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

    """
    This method is used to laod the trained machine learning model and then make the prediction using it and the provided data

    Args:
        data: The data for which the prediction needs to be made

    Returns: Prediction for the provided data
    """
    try:
        # getting the path where the trained model is stored
        config = read_params(config_path)
        model_foldername = config['model']['model_foldername']
        model_name = config['model']['model_name']

        model_path = os.path.join(model_foldername,model_name)

        # loading the trained model
        model = joblib.load(model_path)

        # making the predictions using the preprocessed validated data and the trained model
        prediction = model.predict(data)

        # making the predictions understandable for the user
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

        prediction = thyroid_condition_dict[prediction[0]]

        # returning the predictions
        return prediction
    
    except Exception as e:
        print(f"Error occured in Predict function.")
        raise e

def form_response(dict_request):

    """
    This method is used to validate the data obtained from the user and then preprocess the data using the saved trained preprocess pipeline and 
    finally make the prediction using the trained model.

    Args:
        dict_request: Dictionary containing the inputs provided by the user

    Returns: Response to be displayed to the user
    """

    try:
        # validating the input values entered by the user in the html form using the pydantic library
        validated_inputs = inp_dict_validator(**dict_request)

        # getting the validated dictionary
        input_dict = validated_inputs.dict()

        # creating a dataframe with only one row using the validated dictionary
        data = pd.DataFrame(input_dict,index=[0])

        # getting the path to the stored preprocess pipeline
        config = read_params(config_path)
        preprocess_pipe_foldername = config['preprocess']['preprocess_pipe_foldername']
        preprocess_pipe_filename = config['preprocess']['preprocess_pipe_filename']
        preprocess_pipe_path = os.path.join(preprocess_pipe_foldername, preprocess_pipe_filename)

        # loading the preprocess pipeline 
        with open(preprocess_pipe_path,'rb') as preprocess_file:
            preprocess_pipe = pickle.load(preprocess_file)
        
        # transforming the validated data using the loaded preprocess pipeline
        transformed_data = preprocess_pipe.transform(data)

        # making the prediction using the transformed data and the trained model
        response = Predict(transformed_data)
        return response
        
    except ValidationError as e:
        print(f"Validation error: {str(e)}")
        raise e
        




