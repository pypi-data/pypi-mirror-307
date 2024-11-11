print("""import requests
import pandas as pd

lat = 19.0211
lon = 72.5134

api_key = "14b01e724014c68826132595f1214a55"
api_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"

response = requests.get(api_url)
weather_data = response.json()
weather_data

temperature =  [item['main']['temp'] for item in weather_data['list']]
temperature[-1]

humidity =  [item['main']['humidity'] for item in weather_data['list']]
humidity[-1]

wind_speed = [item['wind']['speed'] for item in weather_data['list']]
wind_speed[-1]

weather_desc = [item['weather'][0]['description'] for item in weather_data['list']]
weather_desc[-1]

date_time = [item['dt_txt'] for item in weather_data['list']]
date_time[-1]

weather_df = pd.DataFrame({'date_time':date_time,
                          'temperature':temperature,
                          'humidity':humidity,
                          'wind_speed':wind_speed,
                          'weather_description':weather_desc})


weather_df.head()


weather_df['date_time'] = pd.to_datetime(weather_df['date_time'])
weather_df['date'] = weather_df['date_time'].dt.date

import matplotlib.pyplot as plt
import seaborn as sns

sns.lineplot(weather_df,x='date_time',y='temperature',label='temp')
sns.lineplot(weather_df,x='date_time',y='wind_speed',label='wind speed')
sns.lineplot(weather_df,x='date_time',y='humidity',label='humidity')
plt.legend()
plt.show()

print(weather_df['temperature'].mean())
weather_df['temperature'].max(),weather_df['temperature'].min()

sns.scatterplot(x=weather_df['temperature'],y=weather_df['humidity'])

weather_df.set_index(weather_df['date_time'],inplace=True)

daily_mean_temp = weather_df['temperature'].resample('D').mean()
daily_mean_humidity = weather_df['humidity'].resample('D').mean()
daily_mean_wind_speed = weather_df['wind_speed'].resample('D').mean()

daily_mean_temp.plot(marker='o')""")


