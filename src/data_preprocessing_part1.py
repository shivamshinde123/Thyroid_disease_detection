
from get_data import read_params
import pandas as pd
import numpy as np

config_path = 'params.yaml'


def remove_unneccessary_columns(lst):
    config = read_params(config_path)
    raw_data = config['data_location']['raw_data']

    df = pd.read_csv(raw_data)

    for feature in lst:
        df.drop(feature, axis=1, inplace=True)


def converting_illogical_ages_to_null():
    config = read_params(config_path)
    raw_data = config['data_location']['raw_data']

    df = pd.read_csv(raw_data)

    df['age'] = np.where((df['age']>100 or df['age']<0), np.nan, df['age'])

def replacing_dash_with_others_in_target_column():

    config = read_params(config_path)
    data_after_preprocess_part1 = config['data_location']['data_after_preprocess_part1']

    df = pd.read_csv(data_after_preprocess_part1)

    df['target'] = np.where(df['target'] == '-', 'Others',df['target'])

    data_after_preprocess_part1 = config['data_location']['data_after_preprocess_part1']
    
    df.to_csv(data_after_preprocess_part1, index=False, sep=',')



if __name__ == '__main__':

    lst = ['patient_id', 'TSH_measured', 'T3_measured', 'TT4_measured', 'T4U_measured','FTI_measured', 'TBG_measured' ]
    remove_unneccessary_columns(lst)
    converting_illogical_ages_to_null()
    replacing_dash_with_others_in_target_column()