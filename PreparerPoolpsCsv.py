import pandas as pd
from utils import get_data


class PreparerPoolpsCsv():
    def __init__(self):
        # Define constant features for every stage of pulpa's preparation
        self.FEATURES_PUPLA_1 = ['Cu_oreth', 'Ni_oreth', 'Ore_mass', 'Mass_1', 'Cu_1.1C', 'Cu_1.1C_max', 'Cu_1.1C_min',
                                 'Cu_1.2C', 'Cu_1.2C_max', 'Cu_1.2C_min', 'Dens_1', 'FM_1.1_A', 'FM_1.2_A', 'Ni_1.1C',
                                 'Ni_1.1C_max', 'Ni_1.1C_min', 'Ni_1.1T_max', 'Ni_1.1T_min', 'Ni_1.2C', 'Ni_1.2C_max',
                                 'Ni_1.2C_min', 'Ni_1.2T_max', 'Ni_1.2T_min']
        self.FEATURES_PUPLA_2 = ['Mass_2', 'Cu_2.1C', 'Cu_2.1C_max', 'Cu_2.1C_min', 'Cu_2.1T', 'Cu_2.1T_max',
                                 'Cu_2.1T_min',
                                 'Cu_2.2C', 'Cu_2.2C_max', 'Cu_2.2C_min', 'Cu_2.2T', 'Cu_2.2T_max', 'Cu_2.2T_min',
                                 'Cu_2F',
                                 'Dens_2', 'FM_2.1_A', 'FM_2.2_A', 'Ni_2.1C', 'Ni_2.1T', 'Ni_2.2C', 'Ni_2.2T', 'Ni_2F']
        self.FEATURES_PUPLA_3 = ['Mass_3', 'Cu_3.1C', 'Cu_3.1C_max', 'Cu_3.1C_min', 'Cu_3.1T', 'Cu_3.1T_max',
                                 'Cu_3.1T_min',
                                 'Cu_3.2C', 'Cu_3.2C_max', 'Cu_3.2C_min', 'Cu_3.2T', 'Cu_3.2T_max', 'Cu_3.2T_min',
                                 'Cu_3F',
                                 'Dens_3', 'FM_3.1_A', 'FM_3.2_A', 'Ni_3.1C', 'Ni_3.1C_max', 'Ni_3.1C_min', 'Ni_3.1T',
                                 'Ni_3.2C', 'Ni_3.2C_max', 'Ni_3.2C_min', 'Ni_3.2T', 'Ni_3F']
        self.FEATURES_PUPLA_4 = ['Mass_4', 'Cu_4F', 'Dens_4', 'FM_4.1_A', 'FM_4.2_A', 'Ni_4.1C', 'Ni_4.1C_max',
                                 'Ni_4.1C_min', 'Ni_4.1T', 'Ni_4.1T_max', 'Ni_4.1T_min', 'Ni_4.2C', 'Ni_4.2C_max',
                                 'Ni_4.2C_min', 'Ni_4.2T', 'Ni_4.2T_max', 'Ni_4.2T_min', 'Ni_4F', 'Vol_4']
        self.FEATURES_PUPLA_5 = ['Mass_5', 'Dens_5', 'FM_5.1_A', 'FM_5.2_A', 'Ni_5.1C', 'Ni_5.1C_max', 'Ni_5.1C_min',
                                 'Ni_5.1T', 'Ni_5.1T_max', 'Ni_5.1T_min', 'Ni_5.2C', 'Ni_5.2C_max', 'Ni_5.2C_min',
                                 'Ni_5.2T',
                                 'Ni_5.2T_max', 'Ni_5.2T_min', 'Ni_5F', 'Vol_5']
        self.FEATURES_PUPLA_6 = ['Mass_6', 'Cu_resth', 'Dens_6', 'FM_6.1_A', 'FM_6.2_A', 'Ni_6.1C', 'Ni_6.1C_max',
                                 'Ni_6.1C_min', 'Ni_6.1T', 'Ni_6.1T_max', 'Ni_6.1T_min', 'Ni_6.2C', 'Ni_6.2C_max',
                                 'Ni_6.2C_min', 'Ni_6.2T', 'Ni_6.2T_max', 'Ni_6.2T_min', 'Ni_6F', 'Ni_rec', 'Ni_resth',
                                 'Vol_6']

        self.data = None
        self.pulpas_df = None

    # data load func
    def load_dataset(self, data: str or pd.DataFrame) -> None:
        if isinstance(data, str):
            self.data = get_data(data)
        elif isinstance(data, pd.DataFrame):
            self.data = data

    # pulpas df preparer
    def prepare_pulpas_dataset(self) -> None:
        results = {}
        c = 0

        df = self.data.reset_index(drop=True)

        # first pulpa made buy first 6 cycles
        pulpa_1 = pd.DataFrame([[df.iloc[0][x] for x in self.FEATURES_PUPLA_1]], columns=self.FEATURES_PUPLA_1)
        pulpa_2 = pd.DataFrame([[df.iloc[1][x] for x in self.FEATURES_PUPLA_2]], columns=self.FEATURES_PUPLA_2)
        pulpa_3 = pd.DataFrame([[df.iloc[2][x] for x in self.FEATURES_PUPLA_3]], columns=self.FEATURES_PUPLA_3)
        pulpa_4 = pd.DataFrame([[df.iloc[3][x] for x in self.FEATURES_PUPLA_4]], columns=self.FEATURES_PUPLA_4)
        pulpa_5 = pd.DataFrame([[df.iloc[4][x] for x in self.FEATURES_PUPLA_5]], columns=self.FEATURES_PUPLA_5)
        pulpa_6 = pd.DataFrame([[df.iloc[5][x] for x in self.FEATURES_PUPLA_6]], columns=self.FEATURES_PUPLA_6)

        # others pulpas processing
        for index, row in df.iloc[6:].iterrows():
            results[c] = pulpa_6
            c += 1
            pulpa_6 = pd.concat(
                [pulpa_5, pd.DataFrame([[row[x] for x in self.FEATURES_PUPLA_6]], columns=self.FEATURES_PUPLA_6)],
                axis=1)
            pulpa_5 = pd.concat(
                [pulpa_4, pd.DataFrame([[row[x] for x in self.FEATURES_PUPLA_5]], columns=self.FEATURES_PUPLA_5)],
                axis=1)
            pulpa_4 = pd.concat(
                [pulpa_3, pd.DataFrame([[row[x] for x in self.FEATURES_PUPLA_4]], columns=self.FEATURES_PUPLA_4)],
                axis=1)
            pulpa_3 = pd.concat(
                [pulpa_2, pd.DataFrame([[row[x] for x in self.FEATURES_PUPLA_3]], columns=self.FEATURES_PUPLA_3)],
                axis=1)
            pulpa_2 = pd.concat(
                [pulpa_1, pd.DataFrame([[row[x] for x in self.FEATURES_PUPLA_2]], columns=self.FEATURES_PUPLA_2)],
                axis=1)
            pulpa_1 = pd.DataFrame([[row[x] for x in self.FEATURES_PUPLA_1]], columns=self.FEATURES_PUPLA_1)

        self.pulpas_df = pd.concat(results, axis=0).reset_index(level=0, drop=True)

    # return pulpas df
    def get_pulpas_df(self) -> pd.DataFrame:
        return self.pulpas_df
