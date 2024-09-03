import requests
import pandas as pd


r = requests.get(
	"http://parkko-api-cleverciti.smartcampus-cloud.de/api/v1/occupancy",
	auth=("parkko_api_user", "0aua2up9awqj7h9tr3dv"),
	params={"before_date": "2024-06-01T12:35:00+02:00"})
text = r.text

newFile = pd.read_json(text)
newFile.to_csv("occupancy.csv")
print(newFile)
