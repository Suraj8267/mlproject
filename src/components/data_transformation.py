## Can do any type of tranformation either it is for categorical feature, numerical feature or handling missing values.
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer  ## To create tranfomation pipeline
from sklearn.impute import SimpleImputer  ## If their is some missing values
from sklearn.pipeline import Pipeline ## o create processing pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

@dataclass
class DataTranformationConfig:  ## Any input that is required for my data transformation component
    preprocessor_ob_file_path = os.path.join("artifacts", "preprocessor.pkl")

from src.utils import save_object

class DataTransformation:
    def __init__(self):
        self.data_tranformation_config = DataTranformationConfig()

    def get_data_tranformer_object(self): ## responsible for creating the pickle file which will be responsible for tranforming the features
        '''
        This function is responsible fo Data Transformtion
        '''
        try:
            numerical_columns = ['writing_score', 'reading_score'] 
            categorical_columns = ["gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]

            num_pipeline = Pipeline(
                steps= [
                    ("imputer", SimpleImputer(strategy='median')),
                    ("Scaler", StandardScaler())
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ("OneHotEncoder", OneHotEncoder()),
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, numerical_columns),
                ("categorical_pipeline", categorical_pipeline, categorical_columns)
            ])

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):  ## it will start the data transformation
        try:
            train_df = pd.read_csv("artifacts/train.csv")
            test_df = pd.read_csv("artifacts/test.csv")

            logging.info("Read Train and Test Data Completed")

            logging.info("Obtaining preprocessing Object")

            preprocessor_obj = self.get_data_tranformer_object()

            target_column_name = "math_score"
            numerical_columns = ['writing_score', 'reading_score'] 

            input_feature_train_df = train_df.drop(columns = [target_column_name], axis= 1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis = 1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe"
            )

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_df, np.array(target_feature_train_df)
            ]  ## np.c_[A, B] : A aur B ko column-wise side-by-side jod do.

            test_arr = np.c_[
                input_feature_test_df, np.array(target_feature_test_df)
            ]

            logging.info(f"Saved Preprocessing object.")

            save_object(

                file_path = self.data_tranformation_config.preprocessor_ob_file_path,
                object= preprocessor_obj
            ) ## used for saving the pickle file



            return (
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_ob_file_path
            )
              
        except Exception as e:
            raise CustomException(e, sys)
            


        