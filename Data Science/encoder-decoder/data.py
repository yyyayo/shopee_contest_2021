import pandas as pd
import torch

SOS_token = 0
EOS_token = 1


class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

def readPOILangs(lang_name):
    print("Reading lines...")

    # Read the file and split into lines
    df_train = pd.read_csv("train.csv")
    raw_addr_train = df_train['raw_address'].tolist()
    df_test = pd.read_csv("test.csv")
    raw_addr_test = df_test['raw_address'].tolist()
    
    POIs = []
    for gt in df_train['POI/street'].tolist():
        POI = gt.split('/', 1)[0]
        POIs.append(POI)

    # Combine addresses and POIs into pairs
    pairs = []
    for i in range(len(raw_addr_train)):
        pairs.append([raw_addr_train[i].replace(",", ""), POIs[i]])
    
    tests = []
    for sent in raw_addr_test:
        tests.append(sent.replace(",",""))
    
    # Reverse pairs, make Lang instances
    lang = Lang(lang_name)

    return lang, pairs, tests

def readStreetLangs(lang_name):
    print("Reading lines...")

    # Read the file and split into lines
    df_train = pd.read_csv("train.csv")
    raw_addr_train = df_train['raw_address'].tolist()
    df_test = pd.read_csv("test.csv")
    raw_addr_test = df_test['raw_address'].tolist()

    streets = []
    for gt in df_train['POI/street'].tolist():
        street = gt.split('/', 1)[1]
        streets.append(street)

    # Combine addresses and POIs into pairs
    pairs = []
    for i in range(len(raw_addr_train)):
        pairs.append([raw_addr_train[i].replace(",", ""), streets[i]])
    
    tests = []
    for sent in raw_addr_test:
        tests.append(sent.replace(",",""))
    
    # Reverse pairs, make Lang instances
    lang = Lang(lang_name)

    return lang, pairs, tests

def prepareData(lang_name, out_name):
    if out_name == 'POI':
        lang, pairs, tests = readPOILangs(lang_name)
    elif out_name == 'street':
        lang, pairs, tests = readStreetLangs(lang_name)
    print("Read %s sentence pairs" % len(pairs))
    print("Read %s testing sentence" % len(tests))
    print("Counting words...")
    for pair in pairs:
        lang.addSentence(pair[0])
        lang.addSentence(pair[1])
    # 取100000个作为此次训练的train，接下来2000个作为验证集validation
    validates = pairs[100000:102000]
    pairs = pairs[:100000]
    # validates = pairs[200000:202000]
    # pairs = pairs[100000:200000]
    # validates = pairs[:2000]
    # pairs = pairs[200000:300000]
    for test in tests:
        lang.addSentence(test)
    print("Counted words:")
    print(lang.name, lang.n_words)
    return lang, pairs, validates, tests

def indexesFromSentence(lang, sentence):
    return [lang.word2index[word] for word in sentence.split(' ')]

def tensorFromSentence(lang, sentence):
    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long).view(-1, 1)

def tensorsFromPair(lang, pair):
    input_tensor = tensorFromSentence(lang, pair[0])
    target_tensor = tensorFromSentence(lang, pair[1])
    return (input_tensor, target_tensor)
