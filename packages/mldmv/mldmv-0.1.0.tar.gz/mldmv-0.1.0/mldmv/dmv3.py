print("""import pandas as pd
import matplotlib.pyplot as plt

churn_df = pd.read_csv('telecom_customer_churn.csv')
churn_df.head()

churn_df.info()

columns = churn_df.columns

def get_sample(df,columns):

    result = {}
    for col in columns:
        result[col] = df[col][:5]

    return result

get_sample(churn_df,columns)

import numpy as np
churn_df.replace(' ',np.nan,inplace=True)
churn_df.replace('?',np.nan,inplace=True)

churn_df.isna().sum()

churn_df['TotalCharges'] = pd.to_numeric(churn_df['TotalCharges'])
churn_df['TotalCharges'].fillna(churn_df['TotalCharges'].mean(),inplace=True)

numeric_col = []

for col in columns:
    if churn_df[col].dtype in ['int64' ,'float64']:
        numeric_col.append(col)

numeric_col = numeric_col[1:]
numeric_col

def show_outliers(df,columns):
    plt.figure(figsize=(10,6 * len(columns)))

    for i,col in enumerate(columns):
        plt.subplot(len(columns),1,i+1)
        plt.boxplot(df[col])
        plt.title(f'boxplot of {col}')
        plt.xlabel(col)

    plt.tight_layout()
    plt.show()

show_outliers(churn_df,numeric_col)

churn_df['Tenure_years'] = churn_df['tenure'] / 12
churn_df['avg_charges_per_month'] = churn_df['TotalCharges'] / churn_df['tenure']

from sklearn.model_selection import train_test_split

columns = churn_df.columns

numeric_columns = []

for col in columns:
    if churn_df[col].dtype in ['int64','float64']:
        numeric_columns.append(col)

numeric_columns

churn_df.drop(columns='customerID',inplace=True)
columns = churn_df.columns


cat_columns = [col for col in columns if col not in numeric_columns]
cat_columns

from sklearn.preprocessing import LabelEncoder

X = churn_df.drop(columns='Churn')
y = churn_df['Churn']

label = LabelEncoder()

for col in cat_columns[:-1]:
    X[col] = label.fit_transform(X[col])

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)


churn_df.to_csv('filtered.csv',index=False)""")