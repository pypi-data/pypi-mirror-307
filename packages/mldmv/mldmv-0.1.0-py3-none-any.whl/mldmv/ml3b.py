print("""import pandas as pd
from sklearn.preprocessing import StandardScaler

social_df = pd.read_csv('Social_Network_Ads.csv')

social_df.drop(columns='User ID',inplace=True)
social_df.head()

classes = ['Male','Female']
labels = [0,1]

social_df['Gender'].replace(classes,labels,inplace=True)
social_df.head()

import seaborn as sns
plt.figure(figsize=(10,6))
plt.subplot(1,2,1)
sns.boxplot(social_df['Age'])

plt.subplot(1,2,2)
sns.boxplot(social_df['EstimatedSalary'])

X = social_df.drop(columns='Purchased')
y = social_df['Purchased']

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay,precision_score,recall_score

X_train,X_test,y_train,y_test = train_test_split(X_scaled,y,test_size=0.3)

param_grid = {
    'n_neighbors': range(1, 20),
    'metric': ['euclidean', 'manhattan']
}

knn = KNeighborsClassifier()
grid_search = GridSearchCV(knn,param_grid,cv=5)

grid_search.fit(X_train,y_train)

best_knn = grid_search.best_estimator_

y_pred = best_knn.predict(X_test)

acc = accuracy_score(y_test,y_pred)

print(acc)
print(1-acc)
precision_score(y_test,y_pred) , recall_score(y_test,y_pred)

cm = confusion_matrix(y_test,y_pred)
c_mat = ConfusionMatrixDisplay(cm)
c_mat.plot()""")


