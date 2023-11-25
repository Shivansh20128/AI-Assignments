from ucimlrepo import fetch_ucirepo 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

scaler = StandardScaler()

abalone = fetch_ucirepo(id=1) 
  
X = abalone.data.features 
y = abalone.data.targets 

categorical_to_int_map = {'M': 2, 'I': -2, 'F': 2}
X['Sex'] = X['Sex'].replace(categorical_to_int_map)

poly = PolynomialFeatures(degree=3)
X = poly.fit_transform(X)

model = LinearRegression()

model.fit(X, y)

y_pred_full = model.predict(X)

r2Score_full = r2_score(y,y_pred_full)

print(f"Full dataset train and eval R2 score: {r2Score_full:.4f}")

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=None)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=None)


pred_training=model.predict(X_train)
r2_train = r2_score(y_train, pred_training)

pred_test=model.predict(X_test)
r2_test = r2_score(y_test, pred_test)
std_test = np.std(pred_test)

pred_val=model.predict(X_val)
r2_val = r2_score(y_val, pred_val)

X = abalone.data.features 
y = abalone.data.targets 
num_iterations = 20

r2_scores_test = []

for _ in range(num_iterations):
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=None)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=None)
    model_new = LinearRegression()

    X_train_normalized = scaler.fit_transform(X_train)
    X_val_normalized = scaler.transform(X_val)
    X_test_normalized = scaler.transform(X_test)

    model_new.fit(X_train_normalized, y_train)

    y_test_pred = model_new.predict(X_test_normalized)

    r2_test = r2_score(y_test, y_test_pred)

    r2_scores_test.append(r2_test)

average_r2 = np.mean(r2_scores_test)
std_dev = np.std(r2_scores_test)
print(f"70-15-15 Cross validation boxplot: mean {average_r2:.4f} std={std_dev:.4f}")