print("""import pandas as pd

sales_df = pd.read_csv('sales_data_sample.csv',encoding='unicode_escape')
sales_df.head()

sales_df.to_json('sales.json')

sales_json_file = pd.read_json('sales.json')
sales_json_file.head()

sales_df.to_excel('sales.xlsx',index=False)

sales_excel_file = pd.read_excel('sales.xlsx')
sales_excel_file.head()

sales_df.drop(columns=['ADDRESSLINE2','STATE'],inplace=True)

sales_df['COUNTRY'].value_counts()

x = sales_df[pd.isna(sales_df['TERRITORY'])]['COUNTRY']
set(x)

label = 'AMERICAS'
import numpy as np
sales_df['TERRITORY'].replace(np.nan,label,inplace=True)

sales_df['TERRITORY'].unique()

sales_df.dropna(inplace=True)

import seaborn as sns 
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
sns.lineplot(y=sales_df['SALES'],x = sales_df['YEAR_ID'])
plt.show()

sns.barplot(x =sales_df['YEAR_ID'],y=sales_df['SALES'])

top_cus = sales_df['CUSTOMERNAME'].value_counts()

plt.figure(figsize=(10,6))
top_cus[:5].plot(kind='bar', color='skyblue')
plt.show()

x = sales_df.groupby('YEAR_ID')['QUANTITYORDERED'].agg(['mean', 'min', 'max'])
x

x.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Year')
plt.ylabel('Value')
plt.xticks(rotation=0)
plt.legend(title='Statistics')
plt.show()""")


