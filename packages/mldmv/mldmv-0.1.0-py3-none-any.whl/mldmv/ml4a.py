print("""import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

iris_df = pd.read_csv('Iris.csv')
iris_df.head()

X = iris_df.drop(columns=['Id','Species'])
X

columns = X.columns
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

filtered_df = remove_outliers(X,columns)
filtered_df

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled[:2]
wcss = []

for i in range(1,11):
    kmeans = KMeans(n_clusters=i)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(wcss,marker='o')
plt.xlabel('number of clusters')
plt.show()

best_kmeans = KMeans(n_clusters=4)
clusters = best_kmeans.fit_predict(X_scaled)
X['cluster_labels'] = clusters

import seaborn as sns
plt.figure(figsize=(8, 5))
sns.scatterplot(x=X_scaled[:, 0], y=X_scaled[:, 1], hue=X['cluster_labels'],palette='Set1',s=100)
plt.title('K-Means Clustering on Iris Dataset')
plt.xlabel('sepal length')
plt.ylabel('sepal width')
plt.legend()
plt.show()""")
