from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from sklearn.linear_model import LogisticRegression
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer


%matplotlib inline

stats = pd.read_csv(os.path.join("csv/MLB DB V1 CSV.csv"))
stats.rename(columns={"O/U Odds": "O/U_Odds"}, inplace=True)

stats.FIELD[stats.FIELD == 'HOME'] = 1
stats.FIELD[stats.FIELD == 'AWAY'] = 0

stats = stats.drop(columns=["Team", "Season", "Date", "Vs", "Score", "Away Starter", "Home Starter",
                            "BAL Line", "O/U", "O/U Result", "Unnamed: 9", "Margin", "Runs Scr", "Runs Alw"])

stats = stats.dropna()

stats.head()

stats.drop(stats[stats["O/U_Odds"] == "9 -"].index, inplace=True)
stats.drop(stats[stats["O/U_Odds"] == "7 -"].index, inplace=True)
stats.drop(stats[stats["O/U_Odds"] == "8 -"].index, inplace=True)
stats.drop(stats[stats["O/U_Odds"] == "10 -"].index, inplace=True)
stats.drop(stats[stats["O/U_Odds"] == "11 -"].index, inplace=True)
stats.drop(stats[stats["O/U_Odds"] == "6 -"].index, inplace=True)

stats.FIELD[stats.FIELD == 'HOME'] = 1
stats.FIELD[stats.FIELD == 'AWAY'] = 0

# Assign X (data) and y (target)
X = stats.drop("Game Result", axis=1)
y = stats["Game Result"]
print(X.shape, y.shape)


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
X_scaler = MinMaxScaler().fit(X_train)
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)


# Step 1: Label-encode data set
label_encoder = LabelEncoder()
label_encoder.fit(y_train)
encoded_y_train = label_encoder.transform(y_train)
encoded_y_test = label_encoder.transform(y_test)

# Step 2: Convert encoded labels to one-hot-encoding
y_train_categorical = to_categorical(encoded_y_train)
y_test_categorical = to_categorical(encoded_y_test)

classifier = LogisticRegression()
classifier

classifier.fit(X_train, y_train)

predictions = classifier.predict(X_test)


model = Sequential()
model.add(Dense(units=100, activation='relu', input_dim=4))
model.add(Dense(units=100, activation='relu'))
model.add(Dense(units=2, activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(
    X_train_scaled,
    y_train_categorical,
    epochs=60,
    shuffle=True,
    verbose=0
)


model_loss, model_accuracy = model.evaluate(
    X_test_scaled, y_test_categorical, verbose=2)
print(
    f"Normal Neural Network - Loss: {model_loss}, Accuracy: {model_accuracy}")
