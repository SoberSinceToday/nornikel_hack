from PreparerPoolpsCsv import  PreparerPoolpsCsv

a = PreparerPoolpsCsv()
a.load_dataset('./data/df_hack_final.csv') # also u can load data as DataFrame like: a.load_dataset(my_df)
a.prepare_pulpas_dataset()
df = a.get_pulpas_df()
print(df.head())