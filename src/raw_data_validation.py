
from cmath import nan
from pydantic import BaseModel, validator, ValidationError
from typing import List
from get_data import read_params
import pandas as pd
import numpy as np

## 1. data type validation
## 2. number of columns validation
## 3. name of columns validation


class Dictvalidator(BaseModel):

    age: int
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
    TSH: float
    T3_measured: str
    T3: float
    TT4_measured: str
    TT4: float
    T4U_measured: str
    T4U: float
    FTI_measured: str
    FTI: float
    TBG_measured: str
    TBG: float
    referral_source: str
    target: str
    patient_id: int

    ## Important: not using following validation functions since these scenatios are convered in data preprocessing stage
    ## The only validation here we are doing is of data type validation

    # @validator('age')
    # def age_validator(cls,v):
    #     if v <= 0 or v > 100:
    #         print('The age value for the row is either less than 0 or greater than 100')
    #     return v
    
    # @validator('sex')
    # def sex_type_validator(cls,v):
    #     if v not in ['M','F',np.nan]:
    #         raise ValueError('Sex should be either M or F')
    #     return v
    
    # @validator('on_thyroxine')
    # def on_thyroxine_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("on_thyroxine value should be either 't' or 'f' ")
    #     return v

    # @validator('query_on_thyroxine')
    # def query_on_thyroxine_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("query_on_thyroxine value should be either 't' or 'f' ")
    #     return v

    # @validator('on_antithyroid_meds')
    # def on_antithyroid_meds_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("on_antithyroid_meds value should be either 't' or 'f' ")
    #     return v

    # @validator('sick')
    # def sick_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("sick value should be either 't' or 'f' ")
    #     return v

    # @validator('pregnant')
    # def pregnant_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("pregnant value should be either 't' or 'f' ")
    #     return v

    # @validator('thyroid_surgery')
    # def thyroid_surgery_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("thyroid_surgery value should be either 't' or 'f' ")
    #     return v

    # @validator('I131_treatment')
    # def I131_treatment_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("I131_treatment value should be either 't' or 'f' ")
    #     return v

    # @validator('query_hypothyroid')
    # def query_hypothyroid_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("query_hypothyroid value should be either 't' or 'f' ")
    #     return v

    # @validator('query_hyperthyroid')
    # def query_hyperthyroid_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("query_hyperthyroid value should be either 't' or 'f' ")
    #     return v

    # @validator('lithium')
    # def lithium_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("lithium value should be either 't' or 'f' ")
    #     return v

    # @validator('goitre')
    # def goitre_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("goitre value should be either 't' or 'f' ")
    #     return v

    # @validator('tumor')
    # def tumor_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("tumor value should be either 't' or 'f' ")
    #     return v

    # @validator('hypopituitary')
    # def hypopituitary_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("hypopituitary value should be either 't' or 'f' ")
    #     return v

    # @validator('psych')
    # def psych_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("psych value should be either 't' or 'f' ")
    #     return v

    # @validator('TSH_measured')
    # def TSH_measured_validator(cls,v):
    #     if v not in ['t','f', np.nan]:
    #         raise ValueError("TSH_measured value should be either 't' or 'f' ")
    #     return v

    # @validator('T3_measured')
    # def T3_measured_validator(cls,v):
    #     if v not in ['t','f',np.nan]:
    #         raise ValueError("T3_measured value should be either 't' or 'f' ")
    #     return v

    # @validator('TT4_measured')
    # def TT4_measured_validator(cls,v):
    #     if v not in ['t','f',np.nan]:
    #         raise ValueError("TT4_measured value should be either 't' or 'f' ")
    #     return v

    # @validator('T4U_measured')
    # def T4U_measured_validator(cls,v):
    #     if v not in ['t','f',np.nan]:
    #         raise ValueError("T4U_measured value should be either 't' or 'f' ")
    #     return v

    # @validator('FTI_measured')
    # def FTI_measured_validator(cls,v):
    #     if v not in ['t','f',np.nan]:
    #         raise ValueError("FTI_measured value should be either 't' or 'f' ")
    #     return v

    # @validator('TBG_measured')
    # def TBG_measured_validator(cls,v):
    #     if v not in ['t','f',np.nan]:
    #         raise ValueError("TBG_measured value should be either 't' or 'f' ")
    #     return v

    # @validator('referral_source')
    # def referral_source_validator(cls,v):
    #     if v not in ['other', 'SVI', 'SVHC', 'STMW', 'SVHD', 'WEST',np.nan]:
    #         raise ValueError("referral_source value should be either of the following: 'other', 'SVI', 'SVHC', 'STMW', 'SVHD', 'WEST'")
    #     return v


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



