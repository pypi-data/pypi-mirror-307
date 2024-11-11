print("""import pandas as pd
df = pd.read_csv('Wine.csv')
df.head()
df['Customer_Segment'].unique()
df.columns
df.isna().sum()
target_column = 'Customer_Segment'

X = df.drop(columns=target_column)
y = df[target_column]

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA()
pca.fit(X_scaled)
exp_var_ratio = pca.explained_variance_ratio_
cumulative_var = exp_var_ratio.cumsum()


plt.plot(range(1,len(cumulative_var)+1),cumulative_var,marker='o')
plt.xlabel('no of components')
plt.ylabel('var ')
plt.grid(True)

pca_new = PCA(n_components=8)
X_pca = pca_new.fit_transform(X_scaled)
plt.scatter(X_pca[:,0],X_pca[:,1],c=y)""")

