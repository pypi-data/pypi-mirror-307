print("""import pandas as pd
diabetes_df = pd.read_csv('diabetes.csv')
diabetes_df.head()

columns = diabetes_df.columns
columns
def univ_analysis(df,columns):

    results = {}

    for col in columns:
        mean = df[col].mean()
        median = df[col].median()
        mode = df[col].mean()
        variance = df[col].var()
        std_dev = df[col].std()
        skewness = df[col].skew()
        kurtosis = df[col].kurtosis()

        results[col] = {'mean':mean,
                        'median':median,
                        'mode':mode,
                        'variance':variance,
                        'standard deviation':std_dev,
                        'skewness':skewness,
                        'kurtosis':kurtosis}
        

    return pd.DataFrame(results)

univ_analysis(diabetes_df,columns)

diabetes_df.info()
columns = columns[:-1]

def remove_outliers(df,columns):

    for col in columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        fil_df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    return fil_df
filtered_df = remove_outliers(diabetes_df,columns)
filtered_df.shape
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.metrics import mean_absolute_error,r2_score,accuracy_score

X = filtered_df.drop(columns='Outcome')
y = filtered_df['Outcome']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)
linear_model = LinearRegression()
linear_model.fit(X_train,y_train)

y_pred = linear_model.predict(X_test)

mean_absolute_error(y_test,y_pred), r2_score(y_test,y_pred)


log_model = LogisticRegression(max_iter=300)
log_model.fit(X_train,y_train)

y_pred = log_model.predict(X_test)

accuracy_score(y_test,y_pred)
import seaborn as sns
import matplotlib.pyplot as plt

corr_matrix = diabetes_df.corr()

plt.figure(figsize=(10,8))
sns.heatmap(corr_matrix,annot=True)
plt.show()""")
