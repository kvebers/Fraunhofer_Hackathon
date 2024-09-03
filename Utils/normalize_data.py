#!/bin/env python3

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
parkhaus_mitte['Normalized'] = (parkhaus_mitte['Procentage'] - parkhaus_mitte['Procentage'].min()) / (parkhaus_mitte['Procentage'].max() - parkhaus_mitte['Procentage'].min())
parkhaus_ost['Normalized'] = (parkhaus_ost['Procentage'] - parkhaus_ost['Procentage'].min()) / (parkhaus_ost['Procentage'].max() - parkhaus_ost['Procentage'].min())
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
parkhaus_mitte['Normalized'].plot(label='Parkhaus Mitte Normalized', color='blue')
plt.title('Normalized Occupancy - Parkhaus Mitte')
plt.xlabel('Time')
plt.ylabel('Normalized Occupancy')
plt.legend()

plt.subplot(2, 1, 2)
parkhaus_ost['Normalized'].plot(label='Parkplatz Ost Normalized', color='blue')
plt.title('Normalized Occupancy - Parkplatz Ost')
plt.xlabel('Time')
plt.ylabel('Normalized Occupancy')
plt.legend()

plt.tight_layout()
plt.show()
