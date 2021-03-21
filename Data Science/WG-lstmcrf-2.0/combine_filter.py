import argparse
import pandas as pd
import numpy as np

def parse_arguments(parser):
    parser.add_argument('--poi', type=str, default="test_POIs.results")
    parser.add_argument('--street', type=str, default="test_streets.results")
    args = parser.parse_args()
    for k in args.__dict__:
        print(k + ": " + str(args.__dict__[k]))
    return args

# def filter(words_dict, abbr):
# 	if abbr in words_dict.keys():
# 		return words_dict[abbr]
# 	else:
# 		return abbr

parser = argparse.ArgumentParser()
args = parse_arguments(parser)

df_POI = pd.read_csv("results/"+args.poi)
df_street = pd.read_csv("results/"+args.street)
# df_words = pd.read_csv("word_extends.csv")

# abbrs = df_words['abbr'].tolist()
# words = df_words['word'].tolist()

# words_list = {}
# for i in range(len(abbrs)):
# 	words_list[abbrs[i]] = words[i]

POIs = df_POI['name'].tolist()
streets = df_street['name'].tolist()

output = []
for i in range(len(POIs)):
	if pd.isnull(POIs[i]):
		POI = ''
	else:
		# POI = filter(words_list, str(POIs[i]))
		POI = str(POIs[i])
	if pd.isnull(streets[i]):
		street = ''
	else:
		# street = filter(words_list, str(streets[i]))
		street = str(streets[i])
	output.append({'id':i, 'POI/street': POI + '/' + street})

df_output = pd.DataFrame(output)

df_output.to_csv("test_answers.csv", columns=('id','POI/street'), index=False)