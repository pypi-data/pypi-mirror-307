print("""import pandas as pd

air_quality_df = pd.read_csv('City_Air_Quality.csv')
air_quality_df.head()

air_quality_df[air_quality_df['AQI']>500]


air_quality_df.isna().sum()

air_quality_df['Date'] = pd.to_datetime(air_quality_df['Date'])

columns = air_quality_df.columns[2:15]
columns

for col in columns:

    air_quality_df[col].fillna(air_quality_df[col].mean(),inplace=True)

import seaborn as sns
import matplotlib.pyplot as plt

ah_df = air_quality_df[air_quality_df['City']=='Ahmedabad']

result = ah_df.groupby('Date')['AQI'].first()

plt.figure(figsize=(20,8))
plt.plot(result.index,result.values)


ah_df = air_quality_df[air_quality_df['City']=='Delhi']

result = ah_df.groupby('Date')['AQI'].first()

plt.figure(figsize=(20,8))
plt.plot(result.index,result.values)

ah_df = air_quality_df[air_quality_df['City']=='Delhi']

result = ah_df.groupby('Date')['PM10'].first()

plt.figure(figsize=(20,8))
plt.plot(result.index,result.values)



ah_df = air_quality_df[air_quality_df['City']=='Delhi']

result = ah_df.groupby('Date')['PM2.5'].first()

plt.figure(figsize=(20,8))
plt.plot(result.index,result.values)

sns.boxplot(air_quality_df[['PM2.5','PM10','NO2']])

plt.show()

sns.scatterplot(air_quality_df,x='AQI',y='PM10',label='PM10',color='red')
sns.scatterplot(air_quality_df,x='AQI',y='PM2.5',label='PM2.5',color='green')

plt.legend()
plt.show()""")




