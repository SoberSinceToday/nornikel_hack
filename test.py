from PreparerPoolpsCsv import PreparerPoolpsCsv
from Solutioner import Solutioner
import warnings

# Отключаем все предупреждения
warnings.filterwarnings("ignore")


a = PreparerPoolpsCsv()
a.load_dataset('./data/df_hack_final.csv')  # also u can load data as DataFrame like: a.load_dataset(my_df)
a.prepare_pulpas_dataset()
df = a.get_pulpas_df()
df.to_csv('./data/pulpas.csv', index=False)

s = Solutioner(path_to_test_data='data/test.csv',
               path_to_train='data/df_hack_final.csv',
               pulpas_df=df)


ans = s.get_ans()
ans.to_csv('data/test.csv', index=False)
