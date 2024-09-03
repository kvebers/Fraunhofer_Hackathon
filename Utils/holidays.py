#!/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


public_holidays_bw_2022 = [
    "2022-01-01",  # New Year's Day
    "2022-01-06",  # Epiphany
    "2022-04-15",  # Good Friday
    "2022-04-18",  # Easter Monday
    "2022-05-01",  # Labour Day
    "2022-05-26",  # Ascension Day
    "2022-06-06",  # Whit Monday
    "2022-06-16",  # Corpus Christi
    "2022-10-03",  # German Unity Day
    "2022-11-01",  # All Saints' Day
    "2022-12-25",  # Christmas Day
    "2022-12-26"   # Boxing Day
]

parkhaus_mitte = pd.read_csv("../data/parkhaus_mitte.csv")
parkhaus_ost = pd.read_csv("../data/parkplatz_ost.csv")
parkhaus_mitte['Date'] = pd.to_datetime(parkhaus_mitte['Date'])
parkhaus_ost['Date'] = pd.to_datetime(parkhaus_ost['Date'])
public_holidays_bw_2022 = pd.to_datetime(public_holidays_bw_2022)
def is_holiday_or_weekend(date):
    if date in public_holidays_bw_2022:
        return 1
    elif date.weekday() >= 5:
        return 1
    else:
        return 0

parkhaus_mitte['Holiday_Weekend'] = parkhaus_mitte['Date'].apply(is_holiday_or_weekend)
parkhaus_ost['Holiday_Weekend'] = parkhaus_ost['Date'].apply(is_holiday_or_weekend)
parkhaus_mitte.to_csv("data/updated_parkhaus_mitte.csv", index=False)
parkhaus_ost.to_csv("data/updated_parkplatz_ost.csv", index=False)
