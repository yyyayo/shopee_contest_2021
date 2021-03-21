import pandas as pd
import re

def makeTest():
	test = pd.read_csv('test.csv')
	test_raw_address = test['raw_address'].tolist()

	raw_address = test['raw_address'].tolist()

	raw_address_words = []
	for i in range(len(raw_address)):
		raw_address[i] = raw_address[i].replace(",", "")
		raw_address_words.append(raw_address[i].split())

	POI_tags = []
	street_tags = []
	for i in range(len(raw_address_words)):
		POI_tag = ['0']*len(raw_address_words[i])
		POI_tags.append(POI_tag)
		street_tag = ['0']*len(raw_address_words[i])
		street_tags.append(street_tag)

	with open("data/POI_ext/test.txt","w") as f:
		for i in range(len(raw_address_words)):
			for j in range(len(raw_address_words[i])):
				f.write(raw_address_words[i][j] + " " + POI_tags[i][j] + "\n")
			f.write("\n")

	with open("data/street_ext/test.txt","w") as f:
		for i in range(len(raw_address_words)):
			for j in range(len(raw_address_words[i])):
				f.write(raw_address_words[i][j] + " " + street_tags[i][j] + "\n")
			f.write("\n") 

def makeTrain():	
	df = pd.read_csv('train.csv')

	df['POI'] = df['POI/street'].str.extract(r'(.*)/', expand=True)
	df['street'] = df['POI/street'].str.extract(r'/(.*)', expand=True)

	raw_address = df['raw_address'].tolist()
	POI = df['POI'].tolist()
	street = df['street'].tolist()

	raw_address_words = []
	POI_words = []
	street_words = []
	for i in range(len(raw_address)):
		raw_address[i] = raw_address[i].replace(",", "")
		raw_address_words.append(raw_address[i].split())
		POI_words.append(POI[i].split())
		street_words.append(street[i].split())

	word_extends = {}
	POI_tags = []
	street_tags = []
	for i in range(len(raw_address_words)):
		POI_tag = ['0']*len(raw_address_words[i])
		if len(POI_words[i]) != 0:
			for j in range(len(raw_address_words[i])):
				if (len(raw_address_words[i][j]) >= 3 and len(POI_words[i][0]) >=3 and raw_address_words[i][j][:3] == POI_words[i][0][:3]) or raw_address_words[i][j] == POI_words[i][0]:
					for m in range(len(POI_words[i])):
						if j+m<len(raw_address_words[i]):
							if raw_address_words[i][j+m] == POI_words[i][m]:
								if m == 0:
									POI_tag[j+m] = 'B-LOC'
								elif m == len(POI_words[i]) - 1:
									POI_tag[j+m] = 'E-LOC'
								else:
									POI_tag[j+m] = 'I-LOC'
							elif len(raw_address_words[i][j+m]) >= 3 and len(POI_words[i][m]) >=3 and raw_address_words[i][j+m][:3] == POI_words[i][m][:3]:
								if m == 0:
									POI_tag[j+m] = 'B-ABBR'
								elif m == len(POI_words[i]) - 1:
									POI_tag[j+m] = 'E-ABBR'
								else:
									POI_tag[j+m] = 'I-ABBR'
								word_extends[raw_address_words[i][j+m]] = POI_words[i][m]
					break
		POI_tags.append(POI_tag)

		street_tag = ['0']*len(raw_address_words[i])
		if len(street_words[i]) != 0:
			for j in range(len(raw_address_words[i])):
				if (len(raw_address_words[i][j]) >= 3 and len(street_words[i][0]) >=3 and raw_address_words[i][j][:3] == street_words[i][0][:3]) or raw_address_words[i][j] == street_words[i][0]:
					for m in range(len(street_words[i])):
						if j+m<len(raw_address_words[i]):
							if raw_address_words[i][j+m] == street_words[i][m]:
								if m == 0:
									street_tag[j+m] = 'B-LOC'
								elif m == len(street_words[i]) - 1:
									street_tag[j+m] = 'E-LOC'
								else:
									street_tag[j+m] = 'I-LOC'
							elif len(raw_address_words[i][j+m]) >= 3 and len(street_words[i][m]) >=3 and raw_address_words[i][j+m][:3] == street_words[i][m][:3]:
								if m == 0:
									street_tag[j+m] = 'B-ABBR'
								elif m == len(street_words[i]) - 1:
									street_tag[j+m] = 'E-ABBR'
								else:
									street_tag[j+m] = 'I-ABBR'
								word_extends[raw_address_words[i][j+m]] = street_words[i][m]
					break
		street_tags.append(street_tag)

	with open("data/POI_ext/train.txt","w") as f:
		for i in range(len(raw_address_words[:270000])):
			for j in range(len(raw_address_words[i])):
				f.write(raw_address_words[i][j] + " " + POI_tags[i][j] + "\n")
			f.write("\n") 

	with open("data/POI_ext/dev.txt","w") as f:
		for i in range(len(raw_address_words[270000:])):
			for j in range(len(raw_address_words[i+270000])):
				f.write(raw_address_words[i+270000][j] + " " + POI_tags[i+270000][j] + "\n")
			f.write("\n") 

	with open("data/street_ext/train.txt","w") as f:
		for i in range(len(raw_address_words[:270000])):
			for j in range(len(raw_address_words[i])):
				f.write(raw_address_words[i][j] + " " + street_tags[i][j] + "\n")
			f.write("\n") 

	with open("data/street_ext/dev.txt","w") as f:
		for i in range(len(raw_address_words[270000:])):
			for j in range(len(raw_address_words[i+270000])):
				f.write(raw_address_words[i+270000][j] + " " + street_tags[i+270000][j] + "\n")
			f.write("\n") 

	with open("word_extends.csv","w") as f:
		f.write(",abbr,word\n")
		i = 0
		for key,value in word_extends.items():
			f.write(str(i)+","+key.replace(",","")+","+value.replace(",","")+"\n")
			i+=1

makeTrain()
makeTest()
# df.to_csv('train_POI_tag.csv', columns=('id', 'raw_address', 'POI'), index=False)
# df.to_csv('train_street_tag.csv', columns=('id', 'raw_address', 'street'), index=False)