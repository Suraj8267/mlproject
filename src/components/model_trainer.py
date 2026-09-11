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
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest": RandomForestRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbours Classifier": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(),
                "AdaBoost Regressior": AdaBoostRegressor()
            }

            params = {
                "Decision Tree": {
                "criterion": ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                # "splitter": ['best', 'random'],
                # "max_features": ['sqrt', 'log2'],
            },
            "Random Forest": {
                # "criterion": ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                # "max_features": ['sqrt', 'log2', None],
                "n_estimators": [8, 16, 32, 64, 128, 256]
            },
            "Gradient Boosting": {
                # "loss": ['squared_error', 'huber', 'absolute_error', 'quantile'],
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
                "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                # "criterion": ['squared_error', 'friedman_mse'],
                # "max_features": ['auto', 'sqrt', 'log2'],
                "n_estimators": [8, 16, 32, 64, 128, 256]
            },
            "Linear Regression": {},
            "K-Neighbour Regressor": {
                'n_neighbors': [5,7,9,11],
                # 'weights': ['uniform', 'distance'],
                # 'algorithm': ['ball_tree', 'kd_tree', 'brute']
            },
            "XGBRegressor": {
                'learning_rate': [.1, .01, .05, .001],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            },
            "CatBoost Regressor": {
                "depth": [6, 8, 10],
                "learning_rate": [0.01, 0.05, 0.1],
                "iterations": [30, 50, 100]
            },

            "AdaBoost Regressor": {
                "learning_rate": [0.1, 0.01, 0.5, 0.001],
                # "loss": ['linear', 'square', 'exponential'],
                "n_estimators": [8, 16, 32, 64, 128, 256]
                }
            }


            model_report: dict = evaluate_models(X_train = X_train,  y_train = y_train, X_test = X_test, y_test = y_test, models = models, param = params) ## Function that returns the finall evalution for all the models

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
