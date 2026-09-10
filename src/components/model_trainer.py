# Multiple regression models ko train/evaluate karna aur best model identify karna.

import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)

from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:  ## Trained Model ko kaha save krna hai 
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainig(self, train_array, test_array):
        try:
            logging.info("Spliting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbours Classifier": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(),
                "AdaBoost Regressior": AdaBoostRegressor()
            }

            model_report: dict = evaluate_models(X_train = X_train,  y_train = y_train, X_test = X_test, y_test = y_test, models = models) ## Function that returns the finall evalution for all the models

            ## To get best model score form the dict
            best_model_score = max(sorted(model_report.values()))   ## sorted: sort in ascending order


            ## To get the best model name from the dict
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]  ## index(best_model_score) : dekho 0.93 kis position par hai: Let 4 the this become list(model_report.keys())[4]

            best_model = models[best_model_name]

            if best_model_score < 0.6:  #  if best_model_score 60 se less aati hai then raise an error
                raise CustomException("No Best Model Found")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path= self.model_trainer_config.trained_model_file_path, 
                object= best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)

            return r2_square
            
        except Exception as e:
            raise CustomException(e, sys)
