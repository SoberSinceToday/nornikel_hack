from utils import *


# Define constants

class Solutioner:
    def __init__(self, path_to_test_data, path_to_train, pulpas_df):
        add_some_notes(pd.read_csv(path_to_test_data)).to_csv(path_to_test_data, index=False)

        self.test_df = pd.read_csv(path_to_test_data)
        self.train_df = pd.read_csv(path_to_train)
        self.pulpas_df = pulpas_df

        # Define constants
        self.STEP1_INPUT = ['Cu_oreth', 'Ni_oreth', 'Ore_mass']  # В тесте достается по таймстемпу
        self.STEP1_PARAMS = ['Cu_1.1C', 'Cu_1.1C_max', 'Cu_1.1C_min', 'Cu_1.2C', 'Cu_1.2C_max', 'Cu_1.2C_min', 'Dens_1',
                             'FM_1.1_A', 'FM_1.2_A', 'Ni_1.1C', 'Ni_1.1C_max', 'Ni_1.1C_min', 'Ni_1.1T_max',
                             'Ni_1.1T_min',
                             'Ni_1.2C', 'Ni_1.2C_max', 'Ni_1.2C_min', 'Ni_1.2T_max',
                             'Ni_1.2T_min']
        self.STEP1_OUT = ['Mass_1']

        self.STEP2_INPUT = self.STEP1_INPUT + self.STEP1_PARAMS + self.STEP1_OUT
        self.STEP2_PARAMS = ['Cu_2.1C', 'Cu_2.1C_max', 'Cu_2.1C_min', 'Cu_2.1T', 'Cu_2.1T_max', 'Cu_2.1T_min',
                             'Cu_2.2C',
                             'Cu_2.2C_max', 'Cu_2.2C_min', 'Cu_2.2T', 'Cu_2.2T_max', 'Cu_2.2T_min', 'Cu_2F', 'Dens_2',
                             'FM_2.1_A', 'FM_2.2_A', 'Ni_2.1C', 'Ni_2.1T', 'Ni_2.2C', 'Ni_2.2T', 'Ni_2F']
        self.STEP2_OUT = ['Mass_2']

        self.STEP3_INPUT = self.STEP2_INPUT + self.STEP2_PARAMS + self.STEP2_OUT
        self.STEP3_PARAMS = ['Cu_3.1C', 'Cu_3.1C_max', 'Cu_3.1C_min', 'Cu_3.1T', 'Cu_3.1T_max', 'Cu_3.1T_min',
                             'Cu_3.2C',
                             'Cu_3.2C_max', 'Cu_3.2C_min', 'Cu_3.2T', 'Cu_3.2T_max', 'Cu_3.2T_min', 'Cu_3F', 'Dens_3',
                             'FM_3.1_A', 'FM_3.2_A', 'Ni_3.1C', 'Ni_3.1T', 'Ni_3.2C', 'Ni_3.2T', 'Ni_3F']
        self.STEP3_OUT = ['Mass_3']

        self.STEP4_INPUT = self.STEP3_INPUT + self.STEP3_PARAMS + self.STEP3_OUT + ['Ni_3.1C_max', 'Ni_3.1C_min',
                                                                                    'Ni_3.2C_max',
                                                                                    'Ni_3.2C_min']
        self.STEP4_PARAMS = ['Cu_4F', 'FM_4.1_A', 'FM_4.2_A', 'Ni_4.1C', 'Ni_4.1C_max', 'Ni_4.1C_min', 'Ni_4.1T',
                             'Ni_4.1T_max', 'Ni_4.1T_min', 'Ni_4.2C', 'Ni_4.2C_max', 'Ni_4.2C_min', 'Ni_4.2T',
                             'Ni_4.2T_max',
                             'Ni_4.2T_min', 'Ni_4F']
        self.STEP4_OUT = ['Mass_4', 'Vol_4', 'Dens_4']

        self.STEP5_INPUT = self.STEP4_INPUT + self.STEP4_PARAMS + self.STEP4_OUT
        self.STEP5_PARAMS = ['FM_5.1_A', 'FM_5.2_A', 'Ni_5.1C', 'Ni_5.1C_max', 'Ni_5.1C_min', 'Ni_5.1T', 'Ni_5.1T_max',
                             'Ni_5.1T_min', 'Ni_5.2C', 'Ni_5.2C_max', 'Ni_5.2C_min', 'Ni_5.2T', 'Ni_5.2T_max',
                             'Ni_5.2T_min',
                             'Ni_5F']
        self.STEP5_OUT = ['Vol_5', 'Mass_5', 'Dens_5']

        self.STEP6_INPUT = self.STEP5_INPUT + self.STEP5_PARAMS + self.STEP5_OUT
        self.STEP6_PARAMS = ['FM_6.1_A', 'FM_6.2_A', 'Ni_6.1C', 'Ni_6.1C_max', 'Ni_6.1C_min', 'Ni_6.1T', 'Ni_6.1T_max',
                             'Ni_6.1T_min', 'Ni_6.2C', 'Ni_6.2C_max', 'Ni_6.2C_min', 'Ni_6.2T', 'Ni_6.2T_max',
                             'Ni_6.2T_min',
                             'Ni_6F']
        self.STEP6_OUT = ['Ni_resth', 'Vol_6', 'Mass_6', 'Cu_resth', 'Dens_6']

        self.TARGET = 'Ni_rec'

    def get_filled_table(self):
        self.test_df = pd.merge(self.train_df[['MEAS_DT', 'Cu_oreth', 'Ni_oreth', 'Ore_mass']], self.test_df,
                                on='MEAS_DT',
                                how='inner')
        self.test_df = self.test_df.reindex(columns=self.train_df.columns)

        # 1st step
        self.test_df = fit_models(inp=self.STEP1_INPUT,
                                  params=self.STEP1_PARAMS,
                                  out=self.STEP1_OUT,
                                  pulpas_df=self.pulpas_df,
                                  test_df=self.test_df)

        # 2-6 steps
        self.test_df = fit_models(inp=self.STEP2_INPUT,
                                  params=self.STEP2_PARAMS,
                                  out=self.STEP2_OUT,
                                  pulpas_df=self.pulpas_df,
                                  test_df=self.test_df)

        self.test_df = fit_models(inp=self.STEP3_INPUT,
                                  params=self.STEP3_PARAMS,
                                  out=self.STEP3_OUT,
                                  pulpas_df=self.pulpas_df,
                                  test_df=self.test_df)

        self.test_df = fit_models(inp=self.STEP4_INPUT,
                                  params=self.STEP4_PARAMS,
                                  out=self.STEP4_OUT,
                                  pulpas_df=self.pulpas_df,
                                  test_df=self.test_df)

        self.test_df = fit_models(inp=self.STEP5_INPUT,
                                  params=self.STEP5_PARAMS,
                                  out=self.STEP5_OUT,
                                  pulpas_df=self.pulpas_df,
                                  test_df=self.test_df)

        self.test_df = fit_models(inp=self.STEP6_INPUT,
                                  params=self.STEP6_PARAMS,
                                  out=self.STEP6_OUT,
                                  pulpas_df=self.pulpas_df,
                                  test_df=self.test_df)

        self.test_df['Ni_rec'] = ni_rec_predict(self.pulpas_df, self.test_df)

        return self.test_df

    def get_ans(self):
        df = self.get_filled_table()
        df = transfrom_ans(df)[5:-6]  # откидываем добавленные 5 строчек сверху и снизу
        return fill_params(df)
