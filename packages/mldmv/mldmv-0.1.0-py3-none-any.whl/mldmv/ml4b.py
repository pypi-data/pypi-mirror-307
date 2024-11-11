print("""import pandas as pd
from sklearn_extra.cluster import KMedoids
import matplotlib.pyplot as plt


credit_df = pd.read_csv('CC GENERAL.csv')
credit_df.head()

credit_df.drop(columns='CUST_ID',inplace=True)

credit_df.describe()
credit_df.isna().sum()

credit_df['MINIMUM_PAYMENTS'].fillna(credit_df['MINIMUM_PAYMENTS'].mean(),inplace=True)
credit_df.dropna(inplace=True)
credit_df.shape

columns = credit_df.columns
columns

def remove_outliers(df,columns):

    for col in columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        fil_df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    return fil_df

filtered_df = remove_outliers(credit_df,columns)
filtered_df.shape

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(filtered_df)


from sklearn.metrics import silhouette_score
sil_scores = []

k = range(2,11)

for i in k :
    kmedoids = KMedoids(n_clusters=i)
    cluster_labels = kmedoids.fit_predict(X_scaled)

    score = silhouette_score(X_scaled,cluster_labels)

    sil_scores.append(score)

plt.plot(k,sil_scores,marker='o')

best_kmeoids = KMedoids(n_clusters=2)
clusters = best_kmeoids.fit_predict(X_scaled)

filtered_df['clusters'] = clusters

import seaborn as sns
sns.scatterplot(x=X_scaled[:,0],y=X_scaled[:,-1],hue=filtered_df['clusters'])""")
