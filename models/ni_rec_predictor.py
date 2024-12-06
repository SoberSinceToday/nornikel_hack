from catboost import CatBoostRegressor
import pandas as pd


class NiRecPredictor:

    def __init__(self) -> None:
        self.TARGET = 'Ni_rec'
        self.data = None
        self.model = None

    # fit model
    def fit(self, data: pd.DataFrame, verbose) -> None:
        self.data = data
        self.model = CatBoostRegressor(iterations=300, objective='RMSE')
        self.model.fit(self.data.drop([self.TARGET], axis=1), self.data[self.TARGET],
                       early_stopping_rounds=50,
                       verbose=verbose, plot=False)

    # get prediction
    def get_predict(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.model.predict(data)

    # save to ./models
    def save_model(self) -> None:
        self.model.save_model('./models/ni_rec_predictor.cbm')
