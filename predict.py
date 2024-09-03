import pandas as pd
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from datetime import timedelta

# Retrieve arguments
month = int(sys.argv[1])
day = int(sys.argv[2])
hour = int(sys.argv[3])
year = 2024
weekday = pd.Timestamp(f"{year}-{month}-{day}").weekday()

# Load the data
parkhaus_mitte = pd.read_csv("data/parkhaus_mitte.csv")
parkhaus_ost = pd.read_csv("data/parkplatz_ost.csv")
parkaus_theresian = pd.read_csv("data/new_data.csv")

# Convert 'Date' column to datetime
parkhaus_mitte['Date'] = pd.to_datetime(parkhaus_mitte['Date'])
parkhaus_ost['Date'] = pd.to_datetime(parkhaus_ost['Date'])
parkaus_theresian['Date'] = pd.to_datetime(parkaus_theresian['Date'])

# Set 'Date' as index
parkhaus_mitte.set_index('Date', inplace=True)
parkhaus_ost.set_index('Date', inplace=True)
parkaus_theresian.set_index('Date', inplace=True)

# Normalize the 'Procentage' column
parkhaus_mitte['Procentage'] = (parkhaus_mitte['Used'] / parkhaus_mitte['Max']) * 100
parkhaus_ost['Procentage'] = (parkhaus_ost['Used'] / parkhaus_ost['Max']) * 100
parkaus_theresian['Procentage'] = (parkaus_theresian['Used'] / parkaus_theresian['Max']) * 100

parkhaus_mitte['Procentage'] = (parkhaus_mitte['Procentage'] - parkhaus_mitte['Procentage'].min()) / (parkhaus_mitte['Procentage'].max() - parkhaus_mitte['Procentage'].min())
parkhaus_ost['Procentage'] = (parkhaus_ost['Procentage'] - parkhaus_ost['Procentage'].min()) / (parkhaus_ost['Procentage'].max() - parkhaus_ost['Procentage'].min())
parkaus_theresian['Procentage'] = (parkaus_theresian['Procentage'] - parkaus_theresian['Procentage'].min()) / (parkaus_theresian['Procentage'].max() - parkaus_theresian['Procentage'].min())

# Extract features
for df in [parkhaus_mitte, parkhaus_ost, parkaus_theresian]:
    df['Month'] = df.index.month
    df['Day'] = df.index.day
    df['Weekday'] = df.index.weekday
    df['Hour'] = df.index.hour

# Prepare training data
X_mitte = parkhaus_mitte[['Month', 'Day', 'Weekday', 'Hour']]
y_mitte = parkhaus_mitte['Procentage']
X_ost = parkhaus_ost[['Month', 'Day', 'Weekday', 'Hour']]
y_ost = parkhaus_ost['Procentage']
X_theresian = parkaus_theresian[['Month', 'Day', 'Weekday', 'Hour']]
y_theresian = parkaus_theresian['Procentage']

# Train/test split
X_train_mitte, X_test_mitte, y_train_mitte, y_test_mitte = train_test_split(X_mitte, y_mitte, test_size=0.2, shuffle=False)
X_train_ost, X_test_ost, y_train_ost, y_test_ost = train_test_split(X_ost, y_ost, test_size=0.2, shuffle=False)
X_train_theresian, X_test_theresian, y_train_theresian, y_test_theresian = train_test_split(X_theresian, y_theresian, test_size=0.2, shuffle=False)

# Train models
model_mitte = XGBRegressor(objective='reg:squarederror', n_estimators=500, learning_rate=0.1)
model_ost = XGBRegressor(objective='reg:squarederror', n_estimators=500, learning_rate=0.1)
model_theresian = XGBRegressor(objective='reg:squarederror', n_estimators=500, learning_rate=0.1)

model_mitte.fit(X_train_mitte, y_train_mitte)
model_ost.fit(X_train_ost, y_train_ost)
model_theresian.fit(X_train_theresian, y_train_theresian)

# Predictions and evaluation
y_pred_mitte = model_mitte.predict(X_test_mitte)
y_pred_ost = model_ost.predict(X_test_ost)
y_pred_theresian = model_theresian.predict(X_test_theresian)

mse_mitte = mean_squared_error(y_test_mitte, y_pred_mitte)
mse_ost = mean_squared_error(y_test_ost, y_pred_ost)
mse_theresian = mean_squared_error(y_test_theresian, y_pred_theresian)

# Predict for the given date
input_features = np.array([[month, day, weekday, hour]])
y_pred_mitte = model_mitte.predict(input_features)
y_pred_ost = model_ost.predict(input_features)
y_pred_theresian = model_theresian.predict(input_features)

min_mitte = parkhaus_mitte['Procentage'].min()
max_mitte = parkhaus_mitte['Procentage'].max()
min_ost = parkhaus_ost['Procentage'].min()
max_ost = parkhaus_ost['Procentage'].max()
min_theresian = parkaus_theresian['Procentage'].min()
max_theresian = parkaus_theresian['Procentage'].max()

def reverseNormalize(x, min, max):
    return x * (max - min) + min


convert_to_predictions_mitte = int(reverseNormalize(y_pred_mitte[0], min_mitte, max_mitte) * 469)
convert_to_predictions_ost = int(reverseNormalize(y_pred_ost[0], min_ost, max_ost) * 120)
convert_to_predictions_theresian = int(reverseNormalize(y_pred_theresian[0], min_theresian, max_theresian) * 365 + 1.9)


output = {
    "mitte": f"{convert_to_predictions_mitte} / 469",
    "ost": f"{convert_to_predictions_ost} / 120",
    "theresian": f"{convert_to_predictions_theresian} / 700"
}

# Print the output as JSON
print(json.dumps(output))
