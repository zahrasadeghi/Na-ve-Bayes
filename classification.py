from collections import *
import json
from arabic_reshaper import arabic_reshaper
from persian_wordcloud.wordcloud import PersianWordCloud
from bidi.algorithm import get_display
from PersianStemmer import PersianStemmer
import random
ps = PersianStemmer()

class1file = "/Users/zahra/Documents/GitHub/Naïve Bayes/data/77.txt"
class2file = "/Users/zahra/Documents/GitHub/Naïve Bayes/data/84-85.txt"

impWOrd85 = {}
impWOrd77 = {}

def randonPartitioner(text, percent):
    firstPartition = text.split(" ")
    partitionedLength = len(firstPartition)
    secondPartiotionLength = int(partitionedLength * percent)
    secondPartiotion = []

    for i in range(secondPartiotionLength):
        r = random.randint(0, partitionedLength -i-1)
        secondPartiotion.append(firstPartition[r])
        del firstPartition[r]
    firstPartitionStringified = ' '.join(firstPartition)
    secondPartiotionStringified = ' '.join(secondPartiotion)
    return firstPartitionStringified, secondPartiotionStringified



def cleanText(text):
    text = text.replace("\n", " ").replace("‌", " ").replace("\r", " ").replace("‎", "").replace("‏", "")
    text = PersianWordCloud.remove_ar(text)
    text = get_display(arabic_reshaper.reshape(ps.run(text)))
    return text


def pClass1(word, countallword1, countDistWords1, class1words):
    if word in class1words.keys():
        return (class1words[word]+1)/(countDistWords1+countallword1)
    else:
        return 1/(countDistWords1+countallword1)

def pClass2(word, countallword2, countDistWords2, class2words):
    if word in class2words.keys():
        return (class2words[word]+1)/(countDistWords2+countallword2)
    else:
        return 1/(countDistWords2+countallword2)


def calculateP(text, pclass1, pclass2, countallword1, countallword2, countDistWords1,countDistWords2,class1words,class2words):
    text = cleanText(text)
    text = text.split("," and "\n" and " " and ":" and "?" and "\"" and "‌" and " ")
    pWordInClass1 = pclass1
    pWordInClass2 = pclass2
    pmax1 = 0
    pmax2 = 0
    for word in text:
        if len(word) < 3:
            continue
        p = pClass1(word, countallword1, countDistWords1, class1words)
        if p > pmax1:
            pmax1 = p
            impword1 = word
        p = pClass2(word, countallword2, countDistWords2, class2words)
        if p > pmax2:
            pmax2 = p
            impword2 = word
        pWordInClass1 *= pClass1(word, countallword1, countDistWords1, class1words)
        pWordInClass2 *= pClass2(word, countallword2, countDistWords2, class2words)
    if pWordInClass1 > pWordInClass2:
        impWOrd77[impword1] = pmax1
        return 1
    else:
        impWOrd85[impword2] = pmax2
        return 2


def countWords(train1, train2):
    train1 = train1.split("," and "\n" and "." and ":" and "?" and "\"" and "‌" and " ")
    counter1 = OrderedDict(Counter(train1))
    train2 = train2.split("," and "\n" and "." and ":" and "?" and "\"" and "‌" and " ")
    counter2 = OrderedDict(Counter(train2))
    return counter1, counter2


def stringifyEvery5Words(arr):
    LEN = int(len(arr) / 50)
    result = []
    for i in range(LEN):
        result.append(" ".join(arr[: 50]))
        del arr[: 50]
    if len(" ".join(arr)):
        result.append(" ".join(arr))
    return result

def classifier():
    class1 = open(class1file).read()
    class2 = open(class2file).read()
    class1 = cleanText(class1)
    class2 = cleanText(class2)
    test1, train1 = randonPartitioner(class1, 0.15)
    test2, train2 = randonPartitioner(class2, 0.3)
    countSentence1 = sum(Counter(train1.split("." and "\n" and "\r" and "?" and "!" and ":")).values())
    countSentence2 = sum(Counter(train2.split("." and "\n" and "\r" and "?" and "!" and ":")).values())
    class1words, class2words = countWords(train1, train2)
    countallword1 = sum(class1words.values())
    countallword2 = sum(class2words.values())
    countDistWords1 = len(class1words.keys())
    countDistWords2 = len(class2words.keys())
    sentence1 = test1.split("." and "\n" and "\r" and "?" and "!" and ":")
    sentence2 = test2.split("." and "\n" and "\r" and "?" and "!" and ":")
    pclass1 = countSentence1/(countSentence1+countSentence2)
    pclass2 = countSentence2/(countSentence1+countSentence2)
    print(pclass2, pclass1)
    tp = 0
    fn = 0
    fp = 0
    tn = 0
    sentence1 = test1.split("." and "\n" and "\r" and "?" and "!" and ":" and " ")
    sentence2 = test2.split("." and "\n" and "\r" and "?" and "!" and ":" and " ")
    sentence1 = stringifyEvery5Words(sentence1)
    sentence2 = stringifyEvery5Words(sentence2)
    print(len(sentence1))
    for sentence in sentence1:
        c = calculateP(sentence, pclass1, pclass2, countallword1, countallword2, countDistWords1, countDistWords2, class1words, class2words)
        if c == 1:
            tp += 1
        else:
            fn += 1
    for sentence in sentence2:
        c = calculateP(sentence, pclass1, pclass2, countallword1, countallword2, countDistWords1, countDistWords2,
                   class1words, class2words)
        if c == 2:
            tn += 1
        else:
            fp += 1

    print(fp, tp, fn, tn)
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    print(precision, recall)
    print(OrderedDict(impWOrd77))
    print(OrderedDict(impWOrd85))

classifier()