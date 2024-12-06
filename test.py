from PreparerPoolpsCsv import  PreparerPoolpsCsv

a = PreparerPoolpsCsv()
a.load_dataset('./data/df_hack_final.csv')
a.prepare_pulpas_dataset()
df = a.get_pulpas_df()
print(df.head())