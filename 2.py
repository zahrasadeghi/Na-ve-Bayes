# -*- coding: utf-8 -*-
from collections import *
import json
from arabic_reshaper import arabic_reshaper
from persian_wordcloud.wordcloud import PersianWordCloud
from bidi.algorithm import get_display
from PersianStemmer import PersianStemmer
import random
ps = PersianStemmer()


class1file = "data/77.txt"
class2file = "data/84-85.txt"


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
    text = arabic_reshaper.reshape(ps.run(text))
    return text


class1 = open(class1file).read()
class2 = open(class2file).read()
class1 = cleanText(class1)
class2 = cleanText(class2)
test1, train1 = randonPartitioner(class1, 0.8)
test2, train2 = randonPartitioner(class2, 0.8)
print(len(test1), len(train1))
countSentence1 = sum(Counter(train1.split("." and "\n" and "\r" and "?" and "!" and ":")).values())
countSentence2 = sum(Counter(train2.split("." and "\n" and "\r" and "?" and "!" and ":")).values())
sentence1 = train1.split("." and "\n" and "\r" and "?" and "!" and "   " and ":")
sentence2 = train2.split("." and "\n" and "\r" and "?" and "!" and "   " and ":")
print(len(sentence1), len(sentence2))
vwString = ""
if len(sentence1) > len(sentence2):
    for i in range(len(sentence2)):
        vwString = vwString + "1|‎" + sentence1[i] + "\n2|‎" + sentence2[i] + "\n"
else:
    for i in range(len(sentence1)):
        vwString = vwString + "1|‎" + sentence1[i] + "\n2|‎" + sentence2[i] + "\n"
print(vwString)
f = open('vw-test', 'w+')
f.write(vwString)
