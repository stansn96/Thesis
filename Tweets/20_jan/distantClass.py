import sys
import string
import os.path

def main():
	file1 = open(sys.argv[1], 'r')
	posfile = open(os.path.dirname(__file__) + '../../Training/Positive/posfile.txt', "a")
	negfile = open(os.path.dirname(__file__) + '../../Training/Negative/negfile.txt', "a")
	poslist = [':)', ':-)', ':d', ';)', '#mooi', '#goed']
	neglist = [':(', ':-(', ":'(", ';(', '#slecht', '#teleurstellend']
	prefixes = ('@', 'http')
	for line in file1:
		tweetcap = line.split('\t')[3]
		tweet = tweetcap.lower()
		tweetlist = list(tweet.split())
		for item in tweetlist[:]:
			if item.startswith(prefixes) or item in string.punctuation or item == "’" or item == "‘":
				tweetlist.remove(item)
		for word in poslist:
			for words in tweetlist:
				if word == words:
					posfile.write(' '.join(tweetlist) + '\n')
		for word in neglist:
			for words in tweetlist:
				if word == words:
					negfile.write(' '.join(tweetlist) + '\n')
	posfile.close()
	negfile.close()

main()
