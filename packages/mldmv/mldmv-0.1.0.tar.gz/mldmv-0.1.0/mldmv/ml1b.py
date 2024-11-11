print("""df = pd.read_csv('Iris.csv')
df.head()

classes = df['Species'].unique().tolist()
classes 
labels = [0,1,2]
df['Species'].replace(classes,labels,inplace=True)

df['Species'].unique()

df.head()

from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

scaler = StandardScaler()
target_column = 'Species'

X = df.drop(columns=[target_column,'Id'])
y = df[target_column]

X_scaled = scaler.fit_transform(X)
X.shape
X_train,X_test,y_train,y_test = train_test_split(X_scaled,y,test_size=0.3)

lda = LinearDiscriminantAnalysis()
lda.fit(X_train,y_train)


y_pred = lda.predict(X_test)
accuracy_score(y_test,y_pred)


import numpy as np
sample = [3.0,2.3,5.5,0.7]

sample = scaler.transform(np.array([sample]))

sample_pred = lda.predict(sample)

classes[sample_pred.tolist()[0]]""")
