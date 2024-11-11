print("""import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier,AdaBoostClassifier
from sklearn.metrics import accuracy_score,r2_score,precision_score

from xgboost import XGBClassifier

iris_df = pd.read_csv('Iris.csv')
iris_df.drop(columns='Id',inplace=True)
iris_df.head()

classes = iris_df['Species'].unique().tolist()
label = [0,1,2]

iris_df['Species'].replace(classes,label,inplace=True)
iris_df.head()

X = iris_df.drop(columns='Species')
y = iris_df['Species']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)

ada_model = AdaBoostClassifier(n_estimators=200)
ada_model.fit(X_train,y_train)


y_pred = ada_model.predict(X_test)

accuracy_score(y_test,y_pred)

gra_model = GradientBoostingClassifier(n_estimators=200)

gra_model.fit(X_train,y_train)

y_pred = gra_model.predict(X_test)

accuracy_score(y_test,y_pred)

xg_model = XGBClassifier(n_estimators=200)

xg_model.fit(X_train,y_train)

y_pred = xg_model.predict(X_test)

accuracy_score(y_test,y_pred)""")
