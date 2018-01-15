import sys
import re
import os
import string
import subprocess
import json

tagDict = {}
for line in open('tagDict'):
    (word, tag) = line.strip().split()
    tagDict[word] = tag

wordClusters = {}
for line in open('60K_clusters.bits.txt'):
    (cluster, word) = line.strip().split()
    wordClusters[word] = []
    for b in [4,8,12]:
        wordClusters[word].append(cluster[0:b])

def GetFeatures(word):
    features = []

    if tagDict.has_key(word):
        features.append("tagDict=%s" % tagDict[word])

    if wordClusters.has_key(word):
        for c in wordClusters[word]:
            features.append("cluster=%s" % c)

    features.append("word=%s" % word)
    features.append("word_lower=%s" % word.lower())
    if(len(word) >= 4):
        features.append("prefix=%s" % word[0:1].lower())
        features.append("prefix=%s" % word[0:2].lower())
        features.append("prefix=%s" % word[0:3].lower())
        features.append("suffix=%s" % word[len(word)-1:len(word)].lower())
        features.append("suffix=%s" % word[len(word)-2:len(word)].lower())
        features.append("suffix=%s" % word[len(word)-3:len(word)].lower())

    if re.search(r'^[A-Z]', word):
        features.append('INITCAP')
    if re.match(r'^[A-Z]+$', word):
        features.append('ALLCAP')
    if re.match(r'.*[0-9].*', word):
        features.append('HASDIGIT')
    if re.match(r'.*[.,;:?!-+\'"].*', word):
        features.append('HASPUNCT')
    return features

class FeatureExtractor:
    def __init__(self):
        self.nf = NerFeatures()

    def Extract(self, words, i):
        features = GetFeatures(words[i])
        #features += self.nf.GetNewFeatures(words[i])
        return features

class NerFeatures:
    def __init__(self):
        self.word2dict = {}
        self.dict = []
        i = 0
        dir="ner"
        for d in os.listdir(dir):
            self.dict.append(d)
            for l in open(dir + "/" + d):
                w = l.rstrip('\n')
                w = w.strip().lower()
                if not self.word2dict.has_key(w):
                    self.word2dict[w] = str(i)
                else:
                    self.word2dict[w] += "\t%s" % i
            i += 1

    def GetNewFeatures(self, line):
        feat=[]
        phrase = line.lower().strip(string.punctuation)
        if self.word2dict.has_key(phrase):
            for dictId in self.word2dict[phrase].split('\t'):
                feat.append('DICTIONARY=%s' % self.dict[int(dictId)])

        return list(feat)