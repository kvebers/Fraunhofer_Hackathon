#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

parkhaus_mitte = pd.read_csv("../data/parkhaus_mitte.csv")
parkhaus_ost = pd.read_csv("../data/parkplatz_ost.csv")

parkhaus_mitte['Date'] = pd.to_datetime(parkhaus_mitte['Date'])
parkhaus_mitte.set_index('Date', inplace=True)
parkhaus_ost['Date'] = pd.to_datetime(parkhaus_ost['Date'])
parkhaus_ost.set_index('Date', inplace=True)

parkhaus_mitte['Procentage'] = (parkhaus_mitte['Used'] / parkhaus_mitte['Max']) * 100
parkhaus_ost['Procentage'] = (parkhaus_ost['Used'] / parkhaus_ost['Max']) * 100

holidays_mitte = parkhaus_mitte[parkhaus_mitte['Holiday_Weekend'] == 1]
holidays_ost = parkhaus_ost[parkhaus_ost['Holiday_Weekend'] == 1]


plt.figure(figsize=(10, 12))

plt.subplot(2, 1, 1)
parkhaus_mitte['Procentage'].plot(label='Parkhaus Mitte', color='blue')
plt.scatter(holidays_mitte.index, holidays_mitte['Procentage'], color='red', marker='o', label='Holidays')
plt.title('Percentage of Occupied Parking Spaces - Parkhaus Mitte')
plt.xlabel('Time')
plt.ylabel('Percentage of Occupied Parking Spaces')
plt.legend()

plt.subplot(2, 1, 2)
parkhaus_ost['Procentage'].plot(label='Parkplatz Ost', color='blue')
plt.scatter(holidays_ost.index, holidays_ost['Procentage'], color='red', marker='o', label='Holidays')
plt.title('Percentage of Occupied Parking Spaces - Parkplatz Ost')
plt.xlabel('Time')
plt.ylabel('Percentage of Occupied Parking Spaces')
plt.legend()

plt.tight_layout()
plt.show()
