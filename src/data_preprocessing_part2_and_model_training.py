
import argparse
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score
from get_data import read_params
import pandas as pd
import numpy as np
import json
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold


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
    data = config['data_location']['data_after_preprocess_part1']

    df = pd.read_csv(data)

    X = df.drop('target',axis=1)
    y = df['target']

    random_state = config['General']['random_state']
    test_size = config['General']['test_size']

    train_X, test_X, train_y, test_y = train_test_split(X, y, random_state=random_state, test_size=test_size)

    ## finding the names of numerical and categorical columns
    cat_cols = [feature for feature in train_X.columns if train_X[feature].dtypes == 'O']
    num_cols = [feature for feature in train_X.columns if feature not in cat_cols]

    ## 1. creating a pipeline to fill the null values and scale the values in categorical columns

    cat_pipe = Pipeline([
        
        ('cat_imputer1', SimpleImputer(missing_values=np.nan, strategy='most_frequent',add_indicator=True)),
        ('cat_encoder', OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=np.nan)),
        ('cat_imputer2', SimpleImputer(missing_values=np.nan, strategy='most_frequent'))
    ])

    ## 2. Creating numerical pipeline

    num_pipe = Pipeline([
        
        # ('num_imputer',KNNImputer(n_neighbors=3, weights="uniform"))
        ('num_imputer',SimpleImputer(missing_values=np.nan, strategy='most_frequent',add_indicator=True))

    ])

    ## 3. Creating a combined pipeline

    preprocess_pipe = ColumnTransformer([
        ('num_pipeline',num_pipe,num_cols),
        ('cat_pipeline',cat_pipe,cat_cols)
    ], remainder='passthrough')

    ## 4. Creating a pipeline for model training
    xgboost_pipe = Pipeline([
    ('xgboost', XGBClassifier(max_depth=2))
    ])

    ## 5. Combining a preprocessing and model training pipelines

    xgboost_pipe = Pipeline([
    ('xgboost_preprocess',preprocess_pipe),
    ('xgboost_model',xgboost_pipe)
    ])

    ## 6. Fitting the model on train data
    xgbc = xgboost_pipe.fit(train_X, train_y)

    ## 7. Predicting metrics using the trained model and the test data

    roc_auc_scr = roc_auc_score(test_y, xgbc.predict_proba(test_X)[:,1])
    classification_rpt = classification_report(test_y, xgbc.predict(test_X), target_names=train_X.unique(),output_dict=True)

    ## 8. Saving the calculated metrics into a json file in the reports folder

    with open('reports/metrics.json','w') as json_file:

        json.dump(classification_rpt, json_file, indent=4)

        roc_auc = dict()
        roc_auc['roc_auc_score'] = roc_auc_scr

        json.dump(roc_auc, json_file, indent=4)

    ## 9. Saving the model in the models folder

    model_foldername = config['model']['model_foldername']
    model_name = config['model']['model_name']

    model_dir = os.path.join(model_foldername, model_name)

    joblib.dump(xgbc, model_dir)



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    model_training(config_path=parsed_args.config)




