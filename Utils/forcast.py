#!/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from datetime import timedelta

parkhaus_mitte = pd.read_csv("../data/parkhaus_mitte.csv")
parkhaus_ost = pd.read_csv("../data/parkplatz_ost.csv")
parkhaus_mitte['Date'] = pd.to_datetime(parkhaus_mitte['Date'])
parkhaus_mitte.set_index('Date', inplace=True)
parkhaus_ost['Date'] = pd.to_datetime(parkhaus_ost['Date'])
parkhaus_ost.set_index('Date', inplace=True)
parkhaus_mitte['Procentage'] = (parkhaus_mitte['Used'] / parkhaus_mitte['Max']) * 100
parkhaus_ost['Procentage'] = (parkhaus_ost['Used'] / parkhaus_ost['Max']) * 100
parkhaus_mitte['Procentage'] = (parkhaus_mitte['Procentage'] - parkhaus_mitte['Procentage'].min()) / (parkhaus_mitte['Procentage'].max() - parkhaus_mitte['Procentage'].min())
parkhaus_ost['Procentage'] = (parkhaus_ost['Procentage'] - parkhaus_ost['Procentage'].min()) / (parkhaus_ost['Procentage'].max() - parkhaus_ost['Procentage'].min())
parkhaus_mitte['Month'] = parkhaus_mitte.index.month
parkhaus_mitte['Day'] = parkhaus_mitte.index.day
parkhaus_mitte['Weekday'] = parkhaus_mitte.index.weekday
parkhaus_mitte['Hour'] = parkhaus_mitte.index.hour
parkhaus_ost['Month'] = parkhaus_ost.index.month
parkhaus_ost['Day'] = parkhaus_ost.index.day
parkhaus_ost['Weekday'] = parkhaus_ost.index.weekday
parkhaus_ost['Hour'] = parkhaus_ost.index.hour
X_mitte = parkhaus_mitte[['Month', 'Day', 'Weekday', 'Hour']]
y_mitte = parkhaus_mitte['Procentage']
X_ost = parkhaus_ost[['Month', 'Day', 'Weekday', 'Hour']]
y_ost = parkhaus_ost['Procentage']
X_train_mitte, X_test_mitte, y_train_mitte, y_test_mitte = train_test_split(X_mitte, y_mitte, test_size=0.2, shuffle=False)
X_train_ost, X_test_ost, y_train_ost, y_test_ost = train_test_split(X_ost, y_ost, test_size=0.2, shuffle=False)
model_mitte = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
model_ost = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
model_mitte.fit(X_train_mitte, y_train_mitte)
model_ost.fit(X_train_ost, y_train_ost)
y_pred_mitte = model_mitte.predict(X_test_mitte)
y_pred_ost = model_ost.predict(X_test_ost)
mse_mitte = mean_squared_error(y_test_mitte, y_pred_mitte)
mse_ost = mean_squared_error(y_test_ost, y_pred_ost)
print(f"Mean Squared Error for Parkhaus Mitte: {mse_mitte:.2f}")
print(f"Mean Squared Error for Parkplatz Ost: {mse_ost:.2f}")
future_dates = pd.date_range(start=parkhaus_mitte.index.max() + timedelta(days=1), periods=730, freq='D')  # 2 years
future_features = pd.DataFrame({
    'Month': future_dates.month,
    'Day': future_dates.day,
    'Weekday': future_dates.weekday,
    'Hour': future_dates.hour
}, index=future_dates)

future_pred_mitte = model_mitte.predict(future_features)
future_pred_ost = model_ost.predict(future_features)
plt.figure(figsize=(14, 10))
plt.subplot(2, 1, 1)
plt.plot(parkhaus_mitte.index, parkhaus_mitte['Procentage'], label='Historical Parkhaus Mitte')
plt.plot(future_dates, future_pred_mitte, label='Forecast Parkhaus Mitte', color='orange')
plt.title('Parkhaus Mitte - Historical and Forecasted Occupancy')
plt.xlabel('Date')
plt.ylabel('Normalized occupancy of the parking space')
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(parkhaus_ost.index, parkhaus_ost['Procentage'], label='Historical Parkplatz Ost')
plt.plot(future_dates, future_pred_ost, label='Forecast Parkplatz Ost', color='orange')
plt.title('Parkplatz Ost - Historical and Forecasted Occupancy')
plt.xlabel('Date')
plt.ylabel('Normalized occupancy of the parking space')
plt.legend()
plt.tight_layout()
plt.show()