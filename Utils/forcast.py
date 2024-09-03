#!/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from datetime import timedelta

# Load datasets
parkhaus_mitte = pd.read_csv("../data/parkhaus_mitte.csv")
parkhaus_ost = pd.read_csv("../data/parkplatz_ost.csv")
parkaus_theresian = pd.read_csv("../data/new_data.csv")

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

print(f"Mean Squared Error for Parkhaus Mitte: {mse_mitte:.2f}")
print(f"Mean Squared Error for Parkplatz Ost: {mse_ost:.2f}")
print(f"Mean Squared Error for Theresian Strasse: {mse_theresian:.2f}")

# Forecast future dates
future_dates = pd.date_range(start=parkhaus_mitte.index.min() + timedelta(days=1), periods=880, freq='D')
future_features = pd.DataFrame({
    'Month': future_dates.month,
    'Day': future_dates.day,
    'Weekday': future_dates.weekday,
    'Hour': future_dates.hour
}, index=future_dates)
parkhaus_mitte.index = parkhaus_mitte.index.tz_localize(None)
parkhaus_ost.index = parkhaus_ost.index.tz_localize(None)
parkaus_theresian.index = parkaus_theresian.index.tz_localize(None)
future_pred_mitte = model_mitte.predict(future_features)
future_pred_ost = model_ost.predict(future_features)
future_pred_theresian = model_theresian.predict(future_features)
# Plot results
plt.figure(figsize=(14, 15))

plt.subplot(3, 1, 1)
plt.plot(parkhaus_mitte.index, parkhaus_mitte['Procentage'], label='Historical Parkhaus Mitte')
plt.plot(future_dates, future_pred_mitte, label='Forecast Parkhaus Mitte', color='orange')
plt.title('Parkhaus Mitte - Historical and Forecasted Occupancy')
plt.xlabel('Date')
plt.ylabel('Normalized occupancy of the parking space')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(parkhaus_ost.index, parkhaus_ost['Procentage'], label='Historical Parkplatz Ost')
plt.plot(future_dates, future_pred_ost, label='Forecast Parkplatz Ost', color='orange')
plt.title('Parkplatz Ost - Historical and Forecasted Occupancy')
plt.xlabel('Date')
plt.ylabel('Normalized occupancy of the parking space')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(parkaus_theresian.index, parkaus_theresian['Procentage'], label='Historical Theresian Strasse')
plt.plot(future_dates, future_pred_theresian, label='Forecast Theresian Strasse', color='orange')
plt.title('Theresian Strasse - Historical and Forecasted Occupancy')
plt.xlabel('Date')
plt.ylabel('Normalized occupancy of the parking space')
plt.legend()

plt.tight_layout()
plt.show()
