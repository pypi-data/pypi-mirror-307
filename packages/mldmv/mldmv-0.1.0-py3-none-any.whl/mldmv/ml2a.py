print("""import pandas as pd

uber_df = pd.read_csv('uber.csv')
uber_df.head()

uber_df.drop(columns='Unnamed: 0',inplace=True)
uber_df.isna().sum()
uber_df.dropna(inplace=True)

lat_to_km = 111
long_to_km = 85

uber_df['manhatten_distance'] = (uber_df['pickup_latitude'] - uber_df['dropoff_latitude']).abs() * lat_to_km + (uber_df['pickup_longitude'] - uber_df['dropoff_longitude']).abs() * long_to_km

uber_df['key'] = pd.to_datetime(uber_df['key'])
uber_df['weekday'] = uber_df['key'].dt.weekday
uber_df['hour'] = uber_df['key'].dt.hour
uber_df.describe()
uber_df = uber_df[uber_df['fare_amount']>0]
uber_df.shape

import matplotlib.pyplot as plt
import seaborn as sns
def uber_boxplot(df_column):

    plt.figure(figsize=(10,6))
    plt.subplot(3,1,1)
    sns.boxplot(uber_df[df_column])
    plt.ylabel(df_column)

    plt.show()


for i in ['fare_amount','passenger_count','manhatten_distance']:
    uber_boxplot(i)

columns_needed = ['fare_amount','passenger_count','manhatten_distance']

def remove_outliers(df,columns):

    for col in columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        fil_df = df[(df[col]>=lower_bound) & (df[col]<=upper_bound)]

    return fil_df
filtered_df = remove_outliers(uber_df,columns_needed)
filtered_df.shape

X = filtered_df[['pickup_longitude',
       'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude',
       'passenger_count', 'manhatten_distance', 'weekday', 'hour']]

y = filtered_df['fare_amount']

from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error,mean_absolute_error
from sklearn.model_selection import train_test_split

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train,X_test,y_train,y_test = train_test_split(X_scaled,y,test_size=0.2)

linear_model = LinearRegression()
linear_model.fit(X_train,y_train)

y_pred = linear_model.predict(X_test)

print(mean_squared_error(y_test,y_pred))
mean_absolute_error(y_test,y_pred)

ridge_model = Ridge(alpha=1)
ridge_model.fit(X_train,y_train)

y_pred = ridge_model.predict(X_test)

print(mean_squared_error(y_test,y_pred))
mean_absolute_error(y_test,y_pred)

lasso_model = Lasso(alpha=1)
lasso_model.fit(X_train,y_train)

y_pred = lasso_model.predict(X_test)

print(mean_squared_error(y_test,y_pred))
mean_absolute_error(y_test,y_pred)""")

