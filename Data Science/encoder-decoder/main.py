from utils import *
from data import *
from model import *
from train_eval import *

import random
import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# torch.cuda.get_device_name(0)

lang, pairs, validates, tests = prepareData('All_words', 'POI')
print(random.choice(pairs))

hidden_size = 256
encoder1 = EncoderRNN(lang.n_words, hidden_size).to(device)
attn_decoder1 = AttnDecoderRNN(hidden_size, lang.n_words, dropout_p=0.1).to(device)

n_iterations = 10000
# encoder1 = torch.load('saved_models/POI-encoder1-%diters-NNN-4.pt'%n_iterations)
# attn_decoder1 = torch.load('saved_models/POI-attn_decoder1-%diters-NNN-4.pt'%n_iterations)
trainIters(encoder1, attn_decoder1, lang, pairs, n_iterations, print_every=1000)
torch.save(encoder1, 'saved_models/POI-encoder1-%diters-1.pt'%n_iterations)
torch.save(attn_decoder1, 'saved_models/POI-attn_decoder1-%diters-1.pt'%n_iterations)