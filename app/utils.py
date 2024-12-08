import pandas as pd
from catboost import CatBoostRegressor, CatBoostClassifier
import numpy as np

# Категориальные фичи
CAT_FEATURES = [
    "FM_6.1_A", "FM_6.2_A",
    "Ni_6.1C_max", "Ni_6.1C_min", "Ni_6.1T_max", "Ni_6.1T_min",
    "Ni_6.2C_max", "Ni_6.2C_min", "Ni_6.2T_max", "Ni_6.2T_min",
    "FM_5.1_A", "FM_5.2_A",
    "Ni_5.1C_max", "Ni_5.1C_min", "Ni_5.1T_max", "Ni_5.1T_min",
    "Ni_5.2C_max", "Ni_5.2C_min", "Ni_5.2T_max", "Ni_5.2T_min",
    "FM_4.1_A", "FM_4.2_A",
    "Ni_4.1C_max", "Ni_4.1C_min", "Ni_4.1T_max", "Ni_4.1T_min",
    "Ni_4.2C_max", "Ni_4.2C_min", "Ni_4.2T_max", "Ni_4.2T_min",
    "Cu_3.1C_max", "Cu_3.1C_min", "Cu_3.1T_max", "Cu_3.1T_min",
    "Cu_3.2C_max", "Cu_3.2C_min", "Cu_3.2T_max", "Cu_3.2T_min",
    "FM_3.1_A", "FM_3.2_A",
    "Ni_3.1C_max", "Ni_3.1C_min", "Ni_3.2C_max", "Ni_3.2C_min",
    "Cu_2.1C_max", "Cu_2.1C_min", "Cu_2.1T_max", "Cu_2.1T_min",
    "Cu_2.2C_max", "Cu_2.2C_min", "Cu_2.2T_max", "Cu_2.2T_min",
    "FM_2.1_A", "FM_2.2_A",
    "Cu_1.1C_max", "Cu_1.1C_min", "Cu_1.2C_max", "Cu_1.2C_min",
    "FM_1.1_A", "FM_1.2_A",
    "Ni_1.1C_max", "Ni_1.1C_min", "Ni_1.1T_max", "Ni_1.1T_min",
    "Ni_1.2C_max", "Ni_1.2C_min", "Ni_1.2T_max", "Ni_1.2T_min"
]

TEST_PARAMS = [
    'Ni_1.1C_min', 'Ni_1.1C_max', 'Cu_1.1C_min', 'Cu_1.1C_max',
    'Ni_1.2C_min', 'Ni_1.2C_max', 'Cu_1.2C_min', 'Cu_1.2C_max',
    'Cu_2.1T_min', 'Cu_2.1T_max', 'Cu_2.2T_min', 'Cu_2.2T_max',
    'Cu_3.1T_min', 'Cu_3.1T_max', 'Cu_3.2T_min', 'Cu_3.2T_max',
    'Ni_4.1T_min', 'Ni_4.1T_max', 'Ni_4.1C_min', 'Ni_4.1C_max',
    'Ni_4.2T_min', 'Ni_4.2T_max', 'Ni_4.2C_min', 'Ni_4.2C_max',
    'Ni_5.1T_min', 'Ni_5.1T_max', 'Ni_5.1C_min', 'Ni_5.1C_max',
    'Ni_5.2T_min', 'Ni_5.2T_max', 'Ni_5.2C_min', 'Ni_5.2C_max',
    'Ni_6.1T_min', 'Ni_6.1T_max', 'Ni_6.1C_min', 'Ni_6.1C_max',
    'Ni_6.2T_min', 'Ni_6.2T_max', 'Ni_6.2C_min', 'Ni_6.2C_max'
]

ITERS = 1  # Итерации для моделей


# data reading
def get_data(path_to_data: str) -> pd.DataFrame:
    data = pd.read_csv(path_to_data)
    data = data[(data['Ni_rec'] < 1) & (data['Ni_rec'] > 0)]
    return data


# Функция для заполнения пропущенных целевых значений медианой
def get_df_to_fit(df, train_features, val_features):
    for feature in val_features:
        df.loc[:, feature] = df[feature].fillna(df[feature].median())
    return df


# Функция для подготовки данных (заполнение пропущенных значений и преобразование категориальных признаков)
def prepare_nans_and_cats(X, y):
    for col in y.columns:
        y.loc[:, col] = y[col].fillna(y[col].median())  # Используем .loc для явного указания

    # Преобразуем категориальные признаки в строки
    for col in CAT_FEATURES:
        if col in X.columns:
            X.loc[:, col] = X[col].astype(str)

    return X, y


# Регрессоры который предиктит все числовые фичи на шаг
def get_regressor(df, X_features, y_features) -> dict:
    X = df[X_features]
    y = df[[x for x in y_features if x not in CAT_FEATURES]]  # выкидываем категориальные
    X, y = prepare_nans_and_cats(X, y)

    models = {}

    for feature in y.columns:
        models[feature] = CatBoostRegressor(iterations=ITERS, objective='RMSE', verbose=0).fit(X, y[feature],
                                                                                               cat_features=[x for x in
                                                                                                             CAT_FEATURES
                                                                                                             if
                                                                                                             x in X_features])
    return models


# Словарь классификаторов категориальных фичей формата {фича: модель_для_предикта_фичи}
def get_classifier(df, X_features, y_features) -> dict:
    X = df[X_features]
    y = df[[x for x in y_features if x in CAT_FEATURES]]  # оставляем категориальные
    X, y = prepare_nans_and_cats(X, y)

    models = {}
    for feature in y.columns:
        models[feature] = CatBoostClassifier(iterations=ITERS,
                                             loss_function='MultiClass',
                                             verbose=False).fit(X, y[feature].astype(str), cat_features=[x
                                                                                                         for
                                                                                                         x in
                                                                                                         CAT_FEATURES
                                                                                                         if
                                                                                                         x in X_features])
    return models


# Возвращает все нужные модельки
def get_models_household(df, inp, step_params, out):
    df_to_fit = get_df_to_fit(df, inp, step_params)
    model_reg = get_regressor(df_to_fit, inp, step_params)
    model_clas = get_classifier(df_to_fit, inp, step_params)
    model_target_regressor = get_regressor(get_df_to_fit(df, inp + step_params, out), inp + step_params, out)
    return model_reg, model_clas, model_target_regressor


# Ф-я для класса
def fit_models(inp: list, params: list, out: list, pulpas_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:
    regressions_params, classifiers_params, model_target = get_models_household(pulpas_df, inp, params, out)

    for f in CAT_FEATURES:
        test_df[f] = test_df[f].astype(str)

    cr, cc = 0, 0
    for param in regressions_params.keys():
        test_df[param] = regressions_params[param].predict(test_df[inp])
        regressions_params[param].save_model(f'./models/regression_{cr}_for_feature_{param}.cbm')
        cr += 1

    for param in classifiers_params.keys():
        test_df[param] = pd.DataFrame(classifiers_params[param].predict(test_df[inp]).flatten().astype(float))
        classifiers_params[param].save_model(f'./models/classifier_{cc}_for_feature{param}.cbm')
        cc += 1

    for f in CAT_FEATURES:
        test_df[f] = test_df[f].astype(str)

    for param in model_target.keys():
        test_df[param] = model_target[param].predict(test_df[inp + params])
        model_target[param].save_model(f'./models/regression_{cr}_for_feature_{param}.cbm')
        cr += 1
    return test_df


def ni_rec_predict(pulpas_df: pd.DataFrame, test_df: pd.DataFrame):
    model = CatBoostRegressor(iterations=300, objective='RMSE')
    model.fit(pulpas_df.drop(['Ni_rec'], axis=1), pulpas_df['Ni_rec'],
              early_stopping_rounds=50,
              verbose=False, plot=False)

    return model.predict(test_df.drop(['MEAS_DT', 'Ni_rec'], axis=1))


# в тесте берем доп 5 строк сверху
def add_some_notes(df) -> pd.DataFrame:
    if df['MEAS_DT'].isin(['2024-01-19 10:45:00']).any(): return df
    meases = ['2024-01-19 10:45:00', '2024-01-19 11:00:00', '2024-01-19 11:15:00', '2024-01-19 11:30:00',
              '2024-01-19 11:45:00', '2024-01-19 12:00:00'][::-1]
    for i in meases:
        new_row = {'MEAS_DT': i}
        all_columns = df.columns.tolist()
        for col in all_columns:
            if col != 'MEAS_DT':
                new_row[col] = np.nan
        new_df = pd.DataFrame([new_row])
        df = pd.concat([new_df, df], ignore_index=True)
    if df['MEAS_DT'].isin(['2024-11-05 18:45:00']).any(): return df
    meases = ['2024-11-05 18:45:00', '2024-11-05 19:00:00', '2024-11-05 19:15:00', '2024-11-05 19:30:00',
              '2024-11-05 19:45:00']
    for i in meases:
        new_row = {'MEAS_DT': i}
        all_columns = df.columns.tolist()
        for col in all_columns:
            if col != 'MEAS_DT':
                new_row[col] = np.nan
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
    return df


def transfrom_ans(df) -> pd.DataFrame:
    STEP1 = [
        'Cu_oreth', 'Ni_oreth', 'Ore_mass',  # STEP1_INPUT
        'Cu_1.1C', 'Cu_1.1C_max', 'Cu_1.1C_min', 'Cu_1.2C', 'Cu_1.2C_max', 'Cu_1.2C_min', 'Dens_1',
        'FM_1.1_A', 'FM_1.2_A', 'Ni_1.1C', 'Ni_1.1C_max', 'Ni_1.1C_min', 'Ni_1.1T_max', 'Ni_1.1T_min',
        'Ni_1.2C', 'Ni_1.2C_max', 'Ni_1.2C_min', 'Ni_1.2T_max', 'Ni_1.2T_min',  # STEP1_PARAMS
        'Mass_1'  # STEP1_OUT
    ]

    STEP2 = [
        'Cu_2.1C', 'Cu_2.1C_max', 'Cu_2.1C_min', 'Cu_2.1T', 'Cu_2.1T_max', 'Cu_2.1T_min', 'Cu_2.2C',
        'Cu_2.2C_max', 'Cu_2.2C_min', 'Cu_2.2T', 'Cu_2.2T_max', 'Cu_2.2T_min', 'Cu_2F', 'Dens_2',
        'FM_2.1_A', 'FM_2.2_A', 'Ni_2.1C', 'Ni_2.1T', 'Ni_2.2C', 'Ni_2.2T', 'Ni_2F',  # STEP2_PARAMS
        'Mass_2'  # STEP2_OUT
    ]

    STEP3 = [
        'Cu_3.1C', 'Cu_3.1C_max', 'Cu_3.1C_min', 'Cu_3.1T', 'Cu_3.1T_max', 'Cu_3.1T_min', 'Cu_3.2C',
        'Cu_3.2C_max', 'Cu_3.2C_min', 'Cu_3.2T', 'Cu_3.2T_max', 'Cu_3.2T_min', 'Cu_3F', 'Dens_3',
        'FM_3.1_A', 'FM_3.2_A', 'Ni_3.1C', 'Ni_3.1T', 'Ni_3.2C', 'Ni_3.2T', 'Ni_3F',  # STEP3_PARAMS
        'Mass_3',  # STEP3_OUT
        'Ni_3.1C_max', 'Ni_3.1C_min', 'Ni_3.2C_max', 'Ni_3.2C_min'  # Дополнительные параметры
    ]

    STEP4 = [
        'Cu_4F', 'FM_4.1_A', 'FM_4.2_A', 'Ni_4.1C', 'Ni_4.1C_max', 'Ni_4.1C_min', 'Ni_4.1T',
        'Ni_4.1T_max', 'Ni_4.1T_min', 'Ni_4.2C', 'Ni_4.2C_max', 'Ni_4.2C_min', 'Ni_4.2T', 'Ni_4.2T_max',
        'Ni_4.2T_min', 'Ni_4F',  # STEP4_PARAMS
        'Mass_4', 'Vol_4', 'Dens_4'  # STEP4_OUT
    ]

    STEP5 = [
        'FM_5.1_A', 'FM_5.2_A', 'Ni_5.1C', 'Ni_5.1C_max', 'Ni_5.1C_min', 'Ni_5.1T', 'Ni_5.1T_max',
        'Ni_5.1T_min', 'Ni_5.2C', 'Ni_5.2C_max', 'Ni_5.2C_min', 'Ni_5.2T', 'Ni_5.2T_max', 'Ni_5.2T_min',
        'Ni_5F',  # STEP5_PARAMS
        'Vol_5', 'Mass_5', 'Dens_5'  # STEP5_OUT
    ]

    STEP6 = [
        'FM_6.1_A', 'FM_6.2_A', 'Ni_6.1C', 'Ni_6.1C_max', 'Ni_6.1C_min', 'Ni_6.1T', 'Ni_6.1T_max',
        'Ni_6.1T_min', 'Ni_6.2C', 'Ni_6.2C_max', 'Ni_6.2C_min', 'Ni_6.2T', 'Ni_6.2T_max', 'Ni_6.2T_min',
        'Ni_6F',  # STEP6_PARAMS
        'Ni_resth', 'Vol_6', 'Mass_6', 'Cu_resth', 'Dens_6',  # STEP6_OUT
        'Ni_rec'  # TARGET
    ]

    df_new = df.copy()
    for index, row in df.iterrows():
        if index < 5: pass
        for param in STEP1:
            df_new.at[index - 5, param] = df.at[index, param]
        for param in STEP2:
            df_new.at[index - 4, param] = df.at[index, param]
        for param in STEP3:
            df_new.at[index - 3, param] = df.at[index, param]
        for param in STEP4:
            df_new.at[index - 2, param] = df.at[index, param]
        for param in STEP5:
            df_new.at[index - 1, param] = df.at[index, param]
        for param in STEP6:
            df_new.at[index, param] = df.at[index, param]

    return df_new[['MEAS_DT'] + TEST_PARAMS]


def fill_params(df):
    for index, row in df.iterrows():
        if index % 8 == 0:
            for param in TEST_PARAMS:
                curr_window = []
                for i in range(8):
                    if index + i < len(df):
                        curr_window.append(float(df.at[index + i, param]))
                    else:
                        break
                for i in range(8):
                    if index + i < len(df):
                        df.at[index + i, param] = np.median(curr_window)
                    else:
                        break

    return df