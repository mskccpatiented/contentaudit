import string
import argparse

try:
	import cPickle as pickle
except:
	import pickle

# Command line interface gubbins
parser = argparse.ArgumentParser(description='Take input filename, outputfile name and threshold')
parser.add_argument('-i','--input', help='Description for foo argument.', required=True)
parser.add_argument('-o','--output', help='Output file name.', required=False)
parser.add_argument('-t','--threshold', help='Commonality threshold.', required=True)
parser.add_argument('-s','--skip', help='Lines to skip', required=False)
args = vars(parser.parse_args())
THRESHOLD = int(args['threshold'])
input = args['input']

# Dictionary of standard English is opened
common_file = 'common.pickle'
pickleFile = open(common_file, 'rb')
common = pickle.load(pickleFile)
pickleFile.close()

# Characters to include or ignore
include = set(string.ascii_letters)
include.add('-')
exclude = set(['\r', '\t', '\n'])
excludewords=set(["tr","td","tdtd","trtd","tdtr","table","span","div","dont","arent","andor","-","sloan-kettering","mskcc","mskccs"])

_file = open(input)
counts = {}

standard = []
jargon = []

linecount = 0
for line in _file.readlines():
	line = line.replace('\r', ' ')
	linecount +=1
	words = line.split(' ')
	if linecount > int(args['skip']):
		for word in words:
			if not word in excludewords:
				if not word.startswith('http') and not word.startswith('www'):
					word = word.strip()
					word =  word.replace('/', ' ')
					word = ''.join(ch for ch in word if ch in include and ch not in exclude)
					if word:
						word = word.lower()
						if word in counts:
							counts[word] = counts[word] + 1
						else:
							counts[word] = 1
							if word in common and common[word] >= THRESHOLD:
								standard.append(word)
							else:
								jargon.append(word)
			

# Output
#print "Standard:", standard
print linecount
print '-------------'
print args['input']
print '-------------'
print "jargonwords:",jargon
#print 'Standard Words:', len(standard)
#print 'Jargon Words:', len(jargon)
print 'jargonpercent:',(float(len(jargon))/float(len(counts))*100)