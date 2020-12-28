import copy
import re
import random


def calculate_uniGram_probability(data):
    prob = {}
    words = []
    for s in data:
        words.append(s.split(' '))
    for w in words:
        for x in w:
            if x == '':
                w.remove('')
    finalWords = []
    for w in words:
        for x in w:
            finalWords.append(x)
    for w in finalWords:
        prob[w] = finalWords.count(w) / len(finalWords)
    print('uniGram process done!')
    return prob
# returns a dictionary with the word as key and probability as value for uniGram


def calculate_biGram_probability(data):
    prob = {}
    words = []
    for d in data:
        words.append(d.split(' '))
    for w in words:
        for x in w:
            if x == '':
                w.remove('')
    finalWords = []
    for w in words:
        for x in w:
            finalWords.append(x)
    for index in range(1, len(finalWords)):
        tmpCountAll = 0
        tmpCount = 0
        for j in range(1, len(finalWords)):
            if finalWords[j - 1] == finalWords[index - 1]:
                tmpCountAll += 1
                if finalWords[j] == finalWords[index]:
                    tmpCount += 1
        prob[finalWords[index - 1], finalWords[index]] = tmpCount / tmpCountAll
    print('biGram process done!')
    return prob
# returns a dictionary with the word as key and probability as value for biGram


def calculate_triGram_probability(data):
    prob = {}
    words = []
    for d in data:
        words.append(d.split(' '))
    for w in words:
        for x in w:
            if x == '':
                w.remove('')
    finalWords = []
    for w in words:
        for x in w:
            finalWords.append(x)
    for index in range(2, len(finalWords)):
        tmpCountAll = 0
        tmpCount = 0
        for j in range(2, len(finalWords)):
            if finalWords[j - 2] == finalWords[index - 2] and finalWords[j - 1] == finalWords[index - 1]:
                tmpCountAll += 1
                if finalWords[j] == finalWords[index]:
                    tmpCount += 1
        prob[finalWords[index - 2], finalWords[index - 1], finalWords[index]] = tmpCount / tmpCountAll
    print('triGram process done!')
    return prob
# returns a dictionary with the word as key and probability as value for triGram


def fix_sentence(inputSentence, mode):
    inputSentence = re.sub('[0-9]' + '.' + '[0-9]', '', inputSentence)  # for deleting '.' in the middle of a number
    inputSentence = re.sub('[0-99999]' + 'th', '', inputSentence)
    inputSentence = re.sub('[!?]', '.', inputSentence)
    inputSentence = re.sub(r'U.S.', 'US', inputSentence)  # for deleting period in the middle of a sentence
    inputSentence = re.sub(r'Ms.', 'Ms', inputSentence)  # for deleting period in the middle of a sentence
    inputSentence = re.sub(r'Mr.', 'Mr', inputSentence)  # for deleting period in the middle of a sentence
    inputSentence = re.sub(r'www.michaelmoore.com', 'michaelmoore', inputSentence)
    inputSentence = re.sub(r'\s+\'', '\'', inputSentence)  # for deleting extra spaces like: don 't
    if mode == 'train':
        inputSentence = re.sub(r'[^A-Za-z. ]', '', inputSentence)
    elif mode == 'test':
        inputSentence = re.sub(r'[^A-Za-z.$ ]', '', inputSentence)
    # deleting everything except words, spaces and periods
    return inputSentence


print('train process started...')
trainFile = open('train.txt', 'r')
sentences = fix_sentence(trainFile.read(), 'train').split('.')
testFile = open('test.txt', 'r', encoding='utf8')
test = testFile.read()
test = fix_sentence(test, 'train').split('.')
for t in test:
    sentences.append(t)
uni = copy.deepcopy(sentences)
bi = copy.deepcopy(sentences)
tri = copy.deepcopy(sentences)
for i in range(len(sentences)):
    bi[i] = ''.join(('<start> ', sentences[i], '<end>'))
    tri[i] = ''.join(('<start0> <start> ', sentences[i], '<end>'))
# now sentences are ready to give to their functions to calculate probabilities
uniGram = calculate_uniGram_probability(uni)
biGram = calculate_biGram_probability(bi)
triGram = calculate_triGram_probability(tri)
# all the n-grams calculated

for t in triGram:
    if t[1:] in biGram and t[2] in uniGram:
        triGram[t] = 0.2 * uniGram[t[2]] + 0.3 * biGram[t[1:]] + 0.5 * triGram[t]
# backOff model calculated
# we can change the coefficients as we want

print('backOff Model is created!')
print('test process started...')
test = open('test.txt', 'r', encoding='utf8').read()
test = fix_sentence(test, 'test').split('.')
previous = []
answers = []
for x in test:
    if x == '':
        test.remove(x)
# test sentences are ready to process

for i in range(len(test) - 1):
    answers.clear()
    previous.clear()
    temp = test[i].split('$')[0].split(' ')
    for t in temp:
        if t == '':
            temp.remove(t)
    maxProb = [None, 0]
    if len(temp) == 0:
        start0 = '<start0>'
        start = '<start>'
    elif len(temp) == 1:
        start0 = '<start0>'
        start = temp.pop()
    else:
        start = temp.pop()
        start0 = temp.pop()

    for u in uniGram:
        if (start0, start, u) in triGram:
            prob = triGram[start0, start, u] * 1000
            round(prob, 3)
            for x in range(int(prob)):
                answers.append(u)
    if len(answers) != 0:
        print(i + 1, ':process done and the deleted word is:', random.choice(answers))
    else:
        print(i + 1, 'process done and no word match!')
