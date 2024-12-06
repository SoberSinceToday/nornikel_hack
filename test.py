import pandas as pd

from PreparerPoolpsCsv import PreparerPoolpsCsv
from models.ni_rec_predictor import NiRecPredictor

# a = PreparerPoolpsCsv()
# a.load_dataset('./data/df_hack_final.csv')  # also u can load data as DataFrame like: a.load_dataset(my_df)
# a.prepare_pulpas_dataset()
# df = a.get_pulpas_df()
# df.to_csv('./data/pulpas.csv')

df = pd.read_csv('./data/pulpas.csv')

ni_rec_predictor = NiRecPredictor()
ni_rec_predictor.fit(df, verbose=False)  # int or bool if u wanna verbose
# ni_rec_predictor.save_model() if u need, saves to ./models
preds = ni_rec_predictor.get_predict(df.drop(['Ni_rec'], axis=1).loc[1])
print(preds)
