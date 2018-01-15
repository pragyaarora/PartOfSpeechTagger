import sys

dictionary={}

for line in open(sys.argv[1]):
    fields = line.strip().split()
    if fields:
        if dictionary.has_key(fields[0]):
            if dictionary[fields[0]].has_key(fields[1]):
                dictionary[fields[0]][fields[1]] += 1
            else:
                dictionary[fields[0]].update({fields[1]:1})
        else:
            dictionary.setdefault(fields[0],{fields[1]:1})

for line in open(sys.argv[2]):
    fields = line.strip().split()
    if fields:
        if dictionary.has_key(fields[0]):
            key, value = max(dictionary[fields[0]].iteritems(), key=lambda p: p[1])
            print fields[0],'',key
        else:
            print fields[0],'','NOUN'
    else:
        print ''