import sys

predicted = []
gold = []

for line in open(sys.argv[1]):
    fields = line.strip().split()
    if len(fields) == 2:
        predicted.append(fields)

for line in open(sys.argv[2]):
    fields = line.strip().split()
    if len(fields) == 2:    
        gold.append(fields)

accuracy = float(len([i for i in range(len(predicted)) if predicted[i][1] == gold[i][1]])) / len(predicted)

#print [(predicted[i], gold[i]) for i in range(len(predicted))]

print "ACCURACY=%s" % accuracy
