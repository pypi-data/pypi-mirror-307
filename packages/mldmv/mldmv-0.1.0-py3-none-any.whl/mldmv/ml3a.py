print("""import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn import datasets

digits = datasets.load_digits()
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X = digits.data
y = digits.target

plt.imshow(digits.images[1],cmap='gray')
X[:2]
set(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train,X_test,y_train,y_test = train_test_split(X_scaled,y,test_size=0.3)

from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,ConfusionMatrixDisplay


svm = SVC(kernel='rbf')

svm.fit(X_train,y_train)

y_pred = svm.predict(X_test)

accuracy_score(y_test,y_pred)

cm = confusion_matrix(y_test,y_pred)

c_mat = ConfusionMatrixDisplay(cm)
c_mat.plot()""")
