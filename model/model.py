import pandas as pd

df = pd.read_csv('../dataset.csv')

# Split dataframes according to their purpose
df_learning = df[df['split'] == 'learning']
df_validating = df[df['split'] == 'validating']
df_testing = df[df['split'] == 'testing']

print(df_learning.head())
print(df_validating.head())
print(df_testing.head())