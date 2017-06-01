import sys
import string

def main():
	file1 = open(sys.argv[1], 'r')
	companyfile = open("companyfile_17_new.txt", "a")
	complist = ['kpn','#kpn','klm','#klm','france-klm','airfrance-klm','airfranceklm','#airfranceklm', 'ing', '#ing', 'shell', '#shell']
	prefixes = ('@', 'http')
	for line in file1:
		tweetcap = line.split('\t')[3]
		tweet = tweetcap.lower()
		tweetlist = list(tweet.split())
		for item in tweetlist[:]:
			if item.startswith(prefixes) or item in string.punctuation or item == "’" or item == "‘":
				tweetlist.remove(item)
		for word in complist:
			for words in tweetlist:
				if word == words:
					companyfile.write(' '.join(tweetlist) + '\n')
	companyfile.close()

main()
