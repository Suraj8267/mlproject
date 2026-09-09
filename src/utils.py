import os
import sys


import numpy as np
import pandas as pd
import dill ## another lib to create pickle file

from src.exception import CustomException

def save_object(file_path, object):
    try: 
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok= True)

        with open(file_path, "wb") as file_obj:
            dill.dump(object, file_obj)  ## Dump obj. into file_obj (preprocessor.pkl)

    except Exception as e:
        raise CustomException(e, sys)