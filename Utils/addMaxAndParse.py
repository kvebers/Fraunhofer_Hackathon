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

cecilienplatz = pd.read_csv("../data/cecilienplatz.csv")