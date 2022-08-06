
from typing import Optional
from pydantic import BaseModel, confloat, validator, conint


class inp_dict_validator(BaseModel):

    age: Optional[conint(gt=0, le=100)]
    sex: Optional[str]
    on_thyroxine: Optional[str]
    query_on_thyroxine: Optional[str]
    on_antithyroid_meds: Optional[str]
    sick: Optional[str]
    pregnant: Optional[str]
    thyroid_surgery: Optional[str]
    I131_treatment: Optional[str]
    query_hypothyroid: Optional[str]
    query_hyperthyroid: Optional[str]
    lithium: Optional[str]
    goitre: Optional[str]
    tumor: Optional[str]
    hypopituitary: Optional[str]
    psych: Optional[str]
    TSH: Optional[confloat(ge=0.005, le=530.0)] 
    T3: Optional[confloat(ge=0.05,le=18.0)] 
    TT4: Optional[confloat(ge=2.0, le=600.0)] 
    T4U: Optional[confloat(ge=0.17, le=2.33)] 
    FTI: Optional[confloat(ge=1.4, le=881.0)] 
    TBG: Optional[confloat(ge=0.1, le=200.0)] 
    referral_source: Optional[str]



    # @validator('sex')
    # def sex_type_validator(cls,v):
    #     if v not in ['M','F']:
    #         raise ValueError('Sex should be either M or F')
    
    # @validator('on_thyroxine','query_on_thyroxine','on_antithyroid_meds','sick','pregnant','thyroid_surgery','I131_treatment','query_hypothyroid','query_hyperthyroid',
    # 'lithium','goitre','tumor','hypopituitary','psych','TSH_measured','T3_measured','TT4_measured','T4U_measured','FTI_measured','TBG_measured')
    # def true_false_validator(cls,v):
    #     if v not in ['t','f']:
    #         raise ValueError('The value should be either t or f')
    #     return v

    # @validator('referral_source')
    # def referral_source_validator(cls,v):
    #     if v not in ['other', 'SVI', 'SVHC', 'STMW', 'SVHD', 'WEST']:
    #         raise ValueError('referral_source value should be either of the following: other, SVI, SVHC, STMW, SVHD, WEST')
    #     return v



    

