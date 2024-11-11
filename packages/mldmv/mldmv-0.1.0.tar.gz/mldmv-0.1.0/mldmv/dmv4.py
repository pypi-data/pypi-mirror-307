print("""import pandas as pd

real_estate_df = pd.read_csv('Bengaluru_House_Data.csv')
real_estate_df.head()

columns = real_estate_df.columns
columns

real_estate_df.isna().sum()

real_estate_df.drop(columns='society',inplace=True)

cols = ['balcony','bath']
for col in cols:
    real_estate_df[col] = real_estate_df[col].fillna(real_estate_df[col].mean())

real_estate_df.dropna(inplace=True)
real_estate_df.shape

real_estate_df['area_type'].unique()


filtered_df = real_estate_df[(real_estate_df['area_type']=='Super built-up  Area') & (real_estate_df['availability']=='Ready To Move')]

real_estate_df['area_type'].unique()

real_estate_df['availability'].unique()

real_estate_df['size'].unique()

for i,value in enumerate(real_estate_df['total_sqft']):
    tokens = str(value).split('-')

    if len(tokens) == 2:

        val = (float(tokens[0]) + float(tokens[1])) / 2
        real_estate_df['total_sqft'].replace(value,int(val),inplace=True)


    if 'Sq. Meter' in str(value):

        index = str(value).find('Sq. Meter')
        val = value[:index]
        val = float(val)*10.7
        real_estate_df['total_sqft'].replace(value,int(val),inplace=True)

    if 'Sq. Yards' in str(value):

        index = str(value).find('Sq. Yards')
        val = value[:index]
        val = float(val)*9
        real_estate_df['total_sqft'].replace(value,int(val),inplace=True)

#Sq. Meter
#Sq. Yards

for i in real_estate_df['total_sqft']:
    if len(str(i)) > 7:
        print(i)

unwanted_units = ['Perch', 'Acres', 'Guntha', 'Cents', 'Grounds']


for i,value in real_estate_df['total_sqft'].items():

    if any(unit in str(value) for unit in unwanted_units):
        real_estate_df.drop(index=i,inplace=True)


real_estate_df.reset_index(drop=True,inplace=True)

real_estate_df['total_sqft'] = pd.to_numeric(real_estate_df['total_sqft'])

real_estate_df.groupby('area_type')['price'].agg(['mean','std'])""")

