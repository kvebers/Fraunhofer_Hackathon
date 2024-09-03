#!/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

public_holidays_bw_2024 = [
    "2024-01-01",
    "2024-01-06",
    "2024-03-29",
    "2024-04-01",
    "2024-05-01",
    "2024-05-09",
    "2024-05-20",
    "2024-05-30",
    "2024-10-03",
    "2024-11-01",
    "2024-12-25",
    "2024-12-26"
]

parkhaus_mitte = pd.read_csv("../data/new_data.csv")
parkhaus_mitte['Date'] = pd.to_datetime(parkhaus_mitte['Date'], utc=True,errors='coerce')
public_holidays_bw_2024 = pd.to_datetime(public_holidays_bw_2024)
def is_holiday_or_weekend(date):
    if date in public_holidays_bw_2024 and date.hour >= 8 and date.hour <= 18:
        return 2
    elif date.weekday() >= 5 and date.hour >= 8 and date.hour <= 22:
        return 1
    else:
        return 0

parkhaus_mitte['Holiday_Weekend'] = parkhaus_mitte['Date'].apply(is_holiday_or_weekend)
parkhaus_mitte['Max'] = 365
parkhaus_mitte.to_csv("../data/new_data.csv", index=False)
