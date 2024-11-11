print("""import pandas as pd
import matplotlib.pyplot as plt

retail_df = pd.read_csv('customer_shopping_data.csv')
retail_df.head()

retail_df.isna().sum()
retail_df.shape

retail_df['total_sale'] = retail_df['quantity'] * retail_df['price']
retail_df.head()

sale_by_region = retail_df.groupby('shopping_mall')['total_sale'].sum()
sale_by_region

import seaborn as sns

plt.figure(figsize=(15,6))
sns.barplot(x = sale_by_region.index,y=sale_by_region.sort_values().values)
plt.ylabel('sales')

sales = retail_df.groupby(['shopping_mall','category'])['total_sale'].first()

sales_df = sales.reset_index()

plt.figure(figsize=(13,6))
sns.barplot(x=sales_df['shopping_mall'],y=sales_df['total_sale'],hue=sales_df['category'])
plt.show()""")

