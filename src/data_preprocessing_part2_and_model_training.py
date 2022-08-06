
import argparse
from sklearn.metrics import balanced_accuracy_score, f1_score, precision_score, recall_score
from get_data import read_params
import pandas as pd
import numpy as np
import json
import os
import joblib
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from xgboost import XGBClassifier


def model_training(config_path):


    """
    This method is performs the following tasks:
    - Splitting the data into training and testing data
    - Imputing the null values from the columns
    - Encoding the categorical values from the categorical columns
    - Training the model using training data
    - Evaluating the model on the testing data
    - Saving the evaluated metrics in a json file 
    - Saving the trained model as a joblib file

    Args:
        config_path: Path to the parameters yaml file
    
    Returns: None

    """

    config = read_params(config_path)
    data = config['data_location']['processed_data']

    df = pd.read_csv(data)
    all_columns = df.columns.values
    all_columns = list(all_columns)
    all_columns = all_columns[:-1]

    X = df.drop('target',axis=1)
    y = df['target']

    random_state = config['General']['random_state']
    test_size = config['General']['test_size']

    train_X, test_X, train_y, test_y = train_test_split(X, y, random_state=random_state, test_size=test_size)

    train_X = pd.DataFrame(train_X, columns=all_columns)
    test_X = pd.DataFrame(test_X, columns=all_columns)

    ## finding the names of numerical and categorical columns
    cat_cols = [feature for feature in train_X.columns if train_X[feature].dtypes == 'O']
    num_cols = [feature for feature in train_X.columns if feature not in cat_cols]

    ## 1. creating a pipeline to fill the null values and scale the values in categorical columns

    cat_pipe = Pipeline([
        
        ('cat_imputer1', SimpleImputer(missing_values=np.nan, strategy='most_frequent',add_indicator=False)),
        ('cat_encoder', OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=np.nan)),
        ('cat_imputer2', SimpleImputer(missing_values=np.nan, strategy='most_frequent'))
    ])

    ## 2. Creating numerical pipeline

    num_pipe = Pipeline([
        ('num_imputer',SimpleImputer(missing_values=np.nan, strategy='most_frequent',add_indicator=False))

    ])

    ## 3. Creating a combined preprocess pipeline, training it and then saving it.

    preprocess_pipe = ColumnTransformer([
        ('num_pipeline',num_pipe,num_cols),
        ('cat_pipeline',cat_pipe,cat_cols)
    ], remainder='passthrough')

    train_X = preprocess_pipe.fit_transform(train_X)
    test_X = preprocess_pipe.transform(test_X)

    preprocess_pipe_foldername = config['preprocess']['preprocess_pipe_foldername']
    preprocess_pipe_filename = config['preprocess']['preprocess_pipe_filename']
    preprocess_pipe_path = os.path.join(preprocess_pipe_foldername, preprocess_pipe_filename)

    with open(preprocess_pipe_path, 'wb') as pickle_file:
        pickle.dump(preprocess_pipe, pickle_file)

    ## saving the final processes data

    final_processed_data_foldername = config['data_location']['processed_data_final_foldername']
    final_processed_data_filename = config['data_location']['processed_data_final_filename']

    if not os.path.exists(final_processed_data_foldername):
        os.mkdir(final_processed_data_foldername)
    
    train_X_dataframe = pd.DataFrame(train_X)
    train_X_dataframe.columns = all_columns
    train_X_dataframe.to_csv(os.path.join(final_processed_data_foldername, final_processed_data_filename), index=False, sep=',')

    ## 4. Creating a pipeline for model training
    xgboost_pipe = Pipeline([
    ('xgboost', XGBClassifier(max_depth=2))
    ])

    ## 5. Fitting the model on train data
    xgbc = xgboost_pipe.fit(train_X, train_y)
    

    ## 6. Predicting metrics using the trained model and the test data
    balanced_accuracy_scr = balanced_accuracy_score(test_y, xgbc.predict(test_X))
    p_scr = precision_score(test_y, xgbc.predict(test_X),average='weighted')
    r_scr = recall_score(test_y, xgbc.predict(test_X),average='weighted')
    f1_scr = f1_score(test_y, xgbc.predict(test_X),average='weighted')

    ## 7. Saving the calculated metrics into a json file in the reports folder
    with open('reports/metrics.json','w') as json_file:
        balanced_accuracy = dict()
        balanced_accuracy['balanced_accuracy_score'] = balanced_accuracy_scr
        balanced_accuracy['precision_score'] = p_scr
        balanced_accuracy['recall_score'] = r_scr
        balanced_accuracy['f1_score'] = f1_scr

        json.dump(balanced_accuracy, json_file, indent=4)

    ## 8. Saving the model in the models folder

    model_foldername = config['model']['model_foldername']
    model_name = config['model']['model_name']

    model_dir = os.path.join(model_foldername, model_name)

    joblib.dump(xgbc, model_dir)

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    model_training(config_path=parsed_args.config)




