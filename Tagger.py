import sys

import numpy as np
import os

from scipy.sparse import csr_matrix
from Data import LinearChainData

class Tagger(object):
    def __init__(self, average=True):
        self.useAveraging = average

    def ComputeThetaAverage(self, u, c):
        self.thetaAverage = self.theta - np.divide(u,c)

    def PrintableSequence(self, sequence):
        return [self.train.tagVocab.GetWord(x) for x in sequence]

    def DumpParameters(self, outFile):
        fOut = open(outFile, 'w')
        sortedParams = (np.argsort(self.thetaAverage, axis=None)[::-1])[0:500]
        for i in sortedParams:
            (tag1ID, tag2ID, featureID) = np.unravel_index(i, self.theta.shape)
            fOut.write("%s %s %s %s\n" % (self.train.tagVocab.GetWord(tag1ID), self.train.tagVocab.GetWord(tag2ID), self.train.vocab.GetWord(featureID), self.thetaAverage[tag1ID,tag2ID,featureID]))
        fOut.close()

    def Train(self, nIter):
        u = np.zeros((self.ntags, self.ntags, self.train.vocab.GetVocabSize()))
        count = 1
        for i in range(nIter):
            nSent = 0
            for (s,g) in self.train.featurizedSentences:
                if len(g) <= 1:         #Skip any length 1 sentences - some numerical issues...
                    continue
                z = self.Viterbi(s, self.theta, len(g))
                sys.stderr.write("Iteration %s, sentence %s\n" % (i, nSent))
                sys.stderr.write("predicted:\t%s\ngold:\t\t%s\n" % (self.PrintableSequence(z), self.PrintableSequence(g)))
                self.UpdateTheta(s,g,z, self.theta, len(g) ,u,count)
                nSent+=1
                count+=1
        if self.useAveraging:
            self.ComputeThetaAverage(u,count)

class ViterbiTagger(Tagger):
    def __init__(self, inFile, average=True):
        self.train = LinearChainData(inFile)
        #print self.train
        self.useAveraging = average

        self.ntags    = self.train.tagVocab.GetVocabSize()
        self.theta    = np.zeros((self.ntags, self.ntags, self.train.vocab.GetVocabSize()))   #T^2 parameter vectors (arc-emission CRF)
        self.thetaSum = np.zeros((self.ntags, self.ntags, self.train.vocab.GetVocabSize()))   #T^2 parameter vectors (arc-emission CRF)
        self.nUpdates = 0

    def TagFile(self, testFile):
        self.test = LinearChainData(testFile, vocab=self.train.vocab)
        #new line
        for i in range(len(self.test.sentences)):
            featurizedSentence = self.test.featurizedSentences[i][0]
            sentence = self.test.sentences[i]
            if self.useAveraging:
                v = self.Viterbi(featurizedSentence, self.thetaAverage, len(sentence))
            else:
                v = self.Viterbi(featurizedSentence, self.theta, len(sentence))
            words = [x[0] for x in sentence]
            tags  = self.PrintableSequence(v)
            for i in range(len(words)):
                print "%s\t%s" % (words[i], tags[i])
            print ""

    def Viterbi(self, featurizedSentence, theta, slen):
        """Viterbi"""
        piMatrix = np.zeros((theta.shape[0],slen+1))
        backPointer = np.zeros((theta.shape[0],slen+1))
        piMatrix[0][0] = 1
        tagVocabLen = len(self.train.tagVocab.id2word)
        startTag = self.train.tagVocab.GetID('START')

        for c in range(1,tagVocabLen):
            piMatrix[c][1] = featurizedSentence[startTag].dot(theta[startTag][c]) + piMatrix[startTag][startTag]
            backPointer[c][1] = startTag

        for i in range(1,slen):
            for c in range(1,tagVocabLen):
                max = float("-inf")
                for p in range(1,tagVocabLen):
                    value = featurizedSentence[i].dot(theta[p][c]) + piMatrix[p][i]
                    if max<value:
                        max = value
                        bp = p
                piMatrix[c][i+1] = max
                backPointer[c][i+1] = bp

        max = -1
        bp = -1
        i = slen
        for k in range(1,tagVocabLen):
            if max < piMatrix[k][slen]:
                max = piMatrix[k][slen]
                bp = k

        viterbiSeq = []
        while i > 0:
            viterbiSeq.append(bp)
            bp = backPointer[bp][i]
            i -= 1

        viterbiSeq.reverse()
        return viterbiSeq

    #Structured Perceptron update
    def UpdateTheta(self, sentenceFeatures, goldSequence, viterbiSequence, theta, slen, u, nSent):

        prevTag1 = self.train.tagVocab.GetID('START')
        prevTag2 = prevTag1

        for i in range(slen):
            features = sentenceFeatures[i]
            currTag1 = goldSequence[i]
            currTag2 = viterbiSequence[i]

            if currTag1 != currTag2:
                theta[prevTag1][currTag1] += features
                theta[prevTag2][currTag2] -= features
                u[prevTag1][currTag1] += (features * nSent)
                u[prevTag2][currTag2] -= (features * nSent)

            prevTag1=currTag1
            prevTag2=currTag2






