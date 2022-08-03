
from cmath import nan
from pydantic import BaseModel, conint, validator, ValidationError
from typing import List, Literal, Optional
from get_data import read_params
import pandas as pd
import numpy as np


class Dictvalidator(BaseModel):

    age: conint(gt=0, le=100)
    sex: str
    on_thyroxine: str
    query_on_thyroxine: str
    on_antithyroid_meds: str
    sick: str
    pregnant: str
    thyroid_surgery: str
    I131_treatment: str
    query_hypothyroid: str
    query_hyperthyroid: str
    lithium: str
    goitre: str
    tumor: str
    hypopituitary: str
    psych: str
    TSH_measured: str
    TSH: Optional[float]
    T3_measured: str
    T3: Optional[float]
    TT4_measured: str
    TT4: Optional[float]
    T4U_measured: str
    T4U: Optional[float]
    FTI_measured: str
    FTI: Optional[float]
    TBG_measured: str
    TBG: Optional[float]
    referral_source: str
    target: str
    patient_id: Optional[int]
    


class dataframe_validator(BaseModel):
    
    df_dict: List[Dictvalidator]



if __name__ == '__main__':
    config_path = 'params.yaml'
    config = read_params(config_path=config_path)
    raw_data = config['data_location']['raw_data']

    df = pd.read_csv(raw_data)
    
    try:
        dataframe_validator(df_dict=df.to_dict(orient='records'))
    except ValidationError as e:
        print(e)



