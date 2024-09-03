import pandas as pd
import sys
import json

# Retrieve arguments
month = sys.argv[1]
day = sys.argv[2]
year = 2024
weekday = pd.Timestamp(f"{year}-{month}-{day}").weekday()








output = {"mitte": f"The prognosis for {month}/{day} is looking good!",
            "ost": f"The prognosis for {month}/{day} is looking good!",
            "theresian": f"The prognosis for {month}/{day} is looking good!"}

# Print the output as JSON
print(json.dumps(output))
