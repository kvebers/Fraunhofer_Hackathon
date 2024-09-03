import pandas as pd
import sys
import json

# Retrieve arguments
month = sys.argv[1]
day = sys.argv[2]

# Example output (replace with your actual logic)
output = {"message": f"The prognosis for {month}/{day} is looking good!"}

# Print the output as JSON
print(json.dumps(output))
