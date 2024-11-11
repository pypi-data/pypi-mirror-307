print("""import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,ConfusionMatrixDisplay,confusion_matrix
from sklearn.preprocessing import LabelEncoder

car_df = pd.read_csv('car_evaluation.csv')
car_df.columns = ['buying_price','maintenance_cost','number_of_doors','number_of_persons','lug_boot','safety','decision']
car_df.head()

car_df.shape

columns = car_df.columns
columns

def unique_values(df,columns):

    results = {}
    for col in columns:
        results[col] = df[col].unique()


    return results

unique_values(car_df,columns)

label_encoder = LabelEncoder()

for col in columns:
    car_df[col] = label_encoder.fit_transform(car_df[col])

car_df.info()

target_column  = 'decision'

X = car_df.drop(columns=target_column)
y = car_df[target_column]

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)

model = RandomForestClassifier(n_estimators=10000)

model.fit(X_train,y_train)

y_pred = model.predict(X_test)

accuracy_score(y_test,y_pred)""")



