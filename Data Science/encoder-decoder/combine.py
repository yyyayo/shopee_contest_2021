import pandas as pd
import numpy as np

# df_POI = pd.read_csv("train_POIs.csv")
# df_street = pd.read_csv("train_streets.csv")
df_POI = pd.read_csv("test_POIs.csv")
df_street = pd.read_csv("test_streets.csv")

POIs = df_POI['POI'].tolist()
streets = df_street['street'].tolist()

output = []
for i in range(len(POIs)):
	if pd.isnull(POIs[i]):
		POI = ''
	else:
		POI = str(POIs[i])
	if pd.isnull(streets[i]):
		street = ''
	else:
		street = str(streets[i])
	output.append({'id':i, 'POI/street': POI + '/' + street})

df_output = pd.DataFrame(output)
# df_output.to_csv("train_answers.csv", columns=('id','POI/street'), index=False)
df_output.to_csv("test_answers.csv", columns=('id','POI/street'), index=False)