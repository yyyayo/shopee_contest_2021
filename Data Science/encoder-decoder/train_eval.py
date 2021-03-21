import pandas as pd
import random
import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import time
from utils import *
from data import *


MAX_LENGTH = 33

teacher_forcing_ratio = 0.5

def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, max_length=MAX_LENGTH):
    encoder_hidden = encoder.initHidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)
    target_length = target_tensor.size(0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

    loss = 0

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]

    decoder_input = torch.tensor([[SOS_token]], device=device)

    decoder_hidden = encoder_hidden

    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False

    if use_teacher_forcing:
        # Teacher forcing: Feed the target as the next input
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            loss += criterion(decoder_output, target_tensor[di])
            decoder_input = target_tensor[di]  # Teacher forcing

    else:
        # Without teacher forcing: use its own predictions as the next input
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            topv, topi = decoder_output.topk(1)
            decoder_input = topi.squeeze().detach()  # detach from history as input

            loss += criterion(decoder_output, target_tensor[di])
            if decoder_input.item() == EOS_token:
                break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_length

def trainIters(encoder, decoder, lang, pairs, n_iters, print_every=1000, plot_every=100, learning_rate=0.01):
    start = time.time()
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
    # training_pairs = [tensorsFromPair(random.choice(pairs))
    #                   for i in range(n_iters)]
    # 修改为打乱的，不用随机
    random.shuffle(pairs)
    training_pairs = [tensorsFromPair(lang, pairs[i]) for i in range(n_iters)]

    criterion = nn.NLLLoss()

    for iter in range(1, n_iters + 1):
        training_pair = training_pairs[iter - 1]
        input_tensor = training_pair[0]
        target_tensor = training_pair[1]

        loss = train(input_tensor, target_tensor, encoder,
                     decoder, encoder_optimizer, decoder_optimizer, criterion)
        print_loss_total += loss
        plot_loss_total += loss

        if iter % print_every == 0:
            print_loss_avg = print_loss_total / print_every
            print_loss_total = 0
            print('%s (%d %d%%) %.4f' % (timeSince(start, iter / n_iters),
                                         iter, iter / n_iters * 100, print_loss_avg))

        if iter % plot_every == 0:
            plot_loss_avg = plot_loss_total / plot_every
            plot_losses.append(plot_loss_avg)
            plot_loss_total = 0

    showPlot(plot_losses)

def evaluate(encoder, decoder, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = tensorFromSentence(lang, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS

        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        return decoded_words, decoder_attentions[:di + 1]

def evaluateRandomly(encoder, decoder, validates, n=20):
    for i in range(n):
        # 取validates验证集来查看
        pair = random.choice(validates)
        print('>', pair[0])
        print('=', pair[1])
        output_words, attentions = evaluate(encoder, decoder, pair[0])
        output_sentence = ' '.join(output_words)
        print('<', output_sentence)
        print('')

def evaluateFixedly(encoder, decoder, validates):
    for i in range(len(validates)):
        # 取validates验证集来查看
        pair = validates[i]
        print('>', pair[0])
        print('=', pair[1])
        output_words, attentions = evaluate(encoder, decoder, pair[0])
        output_sentence = ' '.join(output_words)
        print('<', output_sentence)
        print('')

def evaluateLoss(encoder, decoder, pair, criterion, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = tensorFromSentence(lang, pair[0])
        input_length = input_tensor.size()[0]
        target_tensor = tensorFromSentence(lang, pair[1])
        target_length = target_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS

        decoder_hidden = encoder_hidden

        loss = 0
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            loss += criterion(decoder_output, target_tensor[di])
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                break
            decoder_input = topi.squeeze().detach()

        return loss.item() / target_length

def evaluateAllLoss(encoder, decoder, pairs):
    criterion = nn.NLLLoss()
    loss = 0
    for i in range(len(pairs)):
        loss += evaluateLoss(encoder, decoder, pairs[i], criterion)
    print("Loss is %.4f"%(loss/len(pairs)))

def saveSentence(encoder, decoder, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = tensorFromSentence(lang, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS
        decoder_hidden = encoder_hidden
        decoded_words = []

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                break
            else:
                decoded_words.append(lang.index2word[topi.item()])
            decoder_input = topi.squeeze().detach()

        output_sentence = ' '.join(decoded_words)
        return output_sentence

def saveTrainOutput(encoder, decoder, pairs, name):
    output_sentences = []
    for i, sent in enumerate(pairs):
        if i%10000 == 0:
            print("%d %d%%" % (i, i*100/len(pairs)))
        if name == 'POI':
            output_sentences.append({'POI': saveSentence(encoder, decoder, sent[0])})
        elif name == 'street':
            output_sentences.append({'street': saveSentence(encoder, decoder, sent[0])})
    df_output = pd.DataFrame(output_sentences)
    if name == 'POI':
        df_output.to_csv("saved_answers/train_POIs.csv")
    elif name == 'street':
        df_output.to_csv("saved_answers/train_streets.csv")

def saveValOutput(encoder, decoder, validates, name):
    output_sentences = []
    for i, sent in enumerate(validates):
        if i%5000 == 0:
            print("%d %d%%" % (i, i*100/len(validates)))
        if name == 'POI':
            output_sentences.append({'POI': saveSentence(encoder, decoder, sent[0])})
        elif name == 'street':
            output_sentences.append({'street': saveSentence(encoder, decoder, sent[0])})
    df_output = pd.DataFrame(output_sentences)
    if name == 'POI':
        df_output.to_csv("saved_answers/val_POIs.csv")
    elif name == 'street':
        df_output.to_csv("saved_answers/val_streets.csv")

def saveTestOutput(encoder, decoder, tests, name):
    output_sentences = []
    for i, sent in enumerate(tests):
        if i%5000 == 0:
            print("%d %d%%" % (i, i*100/len(tests)))
        if name == 'POI':
            output_sentences.append({'POI': saveSentence(encoder, decoder, sent)})
        elif name == 'street':
            output_sentences.append({'street': saveSentence(encoder, decoder, sent)})
    df_output = pd.DataFrame(output_sentences)
    if name == 'POI':
        df_output.to_csv("saved_answers/test_POIs.csv")
    elif name == 'street':
        df_output.to_csv("saved_answers/test_streets.csv")