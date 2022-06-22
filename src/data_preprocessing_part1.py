
from get_data import read_params
import pandas as pd
import numpy as np

config_path = 'params.yaml'


def remove_unneccessary_columns(lst):

    """This method is used to remove the column which doesn't contribute to the model training

    Args: List of unneccessary columns 

    Returns: None
    """

    config = read_params(config_path)
    raw_data = config['data_location']['raw_data']
    interim1_data = config['data_location']['interim1_data']

    df = pd.read_csv(raw_data)

    for feature in lst:
        df.drop(feature, axis=1, inplace=True)

    df.to_csv(interim1_data, index=False, sep=',')


def converting_illogical_ages_to_null():

    """This method is used to convert the illogical ages from the data to the null values. This is to be done in order to reduce the false information in the dataset

    Args: None

    Returns: None
    """

    config = read_params(config_path)
    interim1_data = config['data_location']['interim1_data']
    interim2_data = config['data_location']['interim2_data']

    df = pd.read_csv(interim1_data)

    df['age'] = np.where(df['age']>100, np.nan, df['age'])
    df['age'] = np.where(df['age']<0, np.nan, df['age'])

    df.to_csv(interim2_data, index=False, sep=',')

def replacing_dash_with_others_in_target_column():


    """This method is used to replace the '-' value present in the target column with 'Others'

    Args: None

    Returns: None
    """

    config = read_params(config_path)
    interim2_data = config['data_location']['interim2_data']
    processed_data = config['data_location']['processed_data']

    df = pd.read_csv(interim2_data)

    df['target'] = np.where(df['target'] == '-', 'Others',df['target'])
    
    df.to_csv(processed_data, index=False, sep=',')


if __name__ == '__main__':

    lst = ['patient_id', 'TSH_measured', 'T3_measured', 'TT4_measured', 'T4U_measured','FTI_measured', 'TBG_measured' ]
    remove_unneccessary_columns(lst)
    converting_illogical_ages_to_null()
    replacing_dash_with_others_in_target_column()