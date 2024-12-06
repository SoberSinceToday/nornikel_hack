import pandas as pd


# data reading
def get_data(path_to_data: str) -> pd.DataFrame:
    data = pd.read_csv(path_to_data)
    data = data[(data['Ni_rec'] < 1) & (data['Ni_rec'] > 0)]
    return data
