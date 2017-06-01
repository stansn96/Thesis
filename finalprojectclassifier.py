#!/usr/bin/python3

import sys
import string
import nltk.classify
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from featx import bag_of_words, high_information_words
from classification import precision_recall
from random import shuffle
from os import listdir  # to read files
from os.path import isfile, join  # to read files

# return all the filenames in a folder
def get_filenames_in_folder(folder):
	return [f for f in listdir(folder) if isfile(join(folder, f))]


# reads all the files that correspond to the input list of categories and puts their contents in bags of words
def read_files(categories, stopwordsPunctuationList,maptype):
	feats = list()
	print("\n##### Reading", maptype, "files...")
	for category in categories:
		files = get_filenames_in_folder(maptype + '/' + category)
		for tweetsfile in files:
			num_files = 0
			data = open(maptype + '/' + category + '/' + tweetsfile, 'r', encoding='UTF-8').read()
			for line in data.split('\n'):
				tokens = word_tokenize(line)
				filteredTokens = [w for w in tokens if not w in stopwordsPunctuationList and w[0] not in ['/']]
				#print(filteredTokens) 
				bag = bag_of_words(filteredTokens)
				feats.append((bag, category))
				num_files += 1

			print("  Category %s, %i Documents read" % (category, num_files))

	return feats
	
def get_words_in_tweets(feats):
	allwords=[]
	for feat in feats:
		category = feat[1]
		bag = feat[0]
		for w in bag.keys():
			allwords.append(w)
	return allwords

def get_word_features(wordlist):
	featurebag = nltk.FreqDist(wordlist)
	word_features = featurebag.keys()
	return word_features			

def calculate_f(categories, precisions, recalls):
	f_measures = {}
	# calculate the f measure for each category using as input the precisions and recalls
	for category in categories:
		if precisions[category] is None:
			continue
		else:
			f_measures[category] =  (2 * (precisions[category] * recalls[category])) / (precisions[category] + recalls[category])
	return f_measures


# prints accuracy, precision and recall
def evaluation(classifier, test_feats, categories):
	print("\n##### Evaluation...")
	accuracy = nltk.classify.accuracy(classifier, test_feats)
	print("  Accuracy: %f" % accuracy)
	precisions, recalls = precision_recall(classifier, test_feats)
	f_measures = calculate_f(categories, precisions, recalls)

	print(" |-----------|-----------|-----------|-----------|")
	print(" |%-11s|%-11s|%-11s|%-11s|" % ("category","precision","recall","F-measure"))
	print(" |-----------|-----------|-----------|-----------|")
	for category in categories:
		if precisions[category] is None:
			print(" |%-11s|%-11s|%-11s|%-11s|" % (category, "NA", "NA", "NA"))
		else:
			print(" |%-11s|%-11f|%-11f|%-11s|" % (category, precisions[category], recalls[category], f_measures[category]))
	print(" |-----------|-----------|-----------|-----------|")
	return accuracy
		

# show informative features
def analysis(classifier):
	print("\n##### Analysis...")
	classifier.show_most_informative_features(10)


# obtain the high information words
def high_information(feats, categories):
	print("\n##### Obtaining high information words...")

	labelled_words = [(category, []) for category in categories]

	from collections import defaultdict
	words = defaultdict(list)
	all_words = list()
	for category in categories:
		words[category] = list()

	for feat in feats:
		category = feat[1]
		bag = feat[0]
		for w in bag.keys():
			words[category].append(w)
			all_words.append(w)

	labelled_words = [(category, words[category]) for category in categories]

	# Calculate high information words
	high_info_words = set(high_information_words(labelled_words, min_score=12))

	print("  Number of words in the data: %i" % len(all_words))
	print("  Number of distinct words in the data: %i" % len(set(all_words)))
	print("  Number of distinct 'high-information' words in the data: %i" % len(high_info_words))

	return high_info_words


def filter_high_information_words(feats, high_information_words):
	newfeats = []
	dictionary = {}
	for tuple in feats:
		for item in tuple[0].keys():
			if item in high_information_words:
				dictionary[item] = True
		newfeats.append((dictionary, tuple[1]))
		dictionary = {}
	return newfeats
	
def main():
	start_time = time.time()
	stopwordsPunctuationList = stopwords.words('dutch')
	categories = ["Positive","Negative"]
	feats = read_files(categories, stopwordsPunctuationList, 'Training')
	testdatafeats = read_files(categories, stopwordsPunctuationList, 'Test')
	#devdatafeats = read_files(categories, stopwordsPunctuationList, 'Development')
	high_info_words = high_information(feats, categories)
	newfeats = filter_high_information_words(feats, high_info_words)
	accuracylist = []
	
	def extract_features(document):
		document_words = set(document)
		features = {}
		for word in word_features:
			if word in document_words:
				features['contains(%s)' % word] = True
		return features
		
	word_features = get_word_features(get_words_in_tweets(newfeats))
	training_set = nltk.classify.apply_features(extract_features, newfeats)
	classifier = nltk.classify.NaiveBayesClassifier.train(training_set)
	print("--- %s seconds ---" % (time.time() - start_time))
	dev_set = nltk.classify.apply_features(extract_features, testdatafeats)
	accuracylist.append(evaluation(classifier, dev_set, categories))
	analysis(classifier)

	KpnTriggers = ['kpn','#kpn']
	KlmTriggers = ['klm','#klm','france-klm','airfrance-klm','airfranceklm','#airfranceklm']
	INGTriggers = ['ing', '#ing']
	ShellTriggers = ['shell', '#shell']

	twitterData = ["companies_16_new.txt", "companies_17_new.txt", "companies_18_new.txt", "companies_19_new.txt", "companies_20_new.txt", "companies_21_new.txt", "companies_22_new.txt", "companies_23_new.txt", "companies_24_new.txt", "companies_25_new.txt", "companies_26_new.txt", "companies_27_new.txt"]
	for testfile in twitterData:
		counter=0
		positiveKpn, negativeKpn = 0,0
		positiveKlm, negativeKlm = 0,0
		positiveING, negativeING = 0,0
		positiveShell, negativeShell = 0,0
		with open('Research/' + testfile, "r") as researchfile:
			for line in researchfile:
				for item in KpnTriggers:
					if item in line.split():
						result = classifier.prob_classify(extract_features(line.split()))
						if result.max() == "Positive" and result.prob("Positive") >= 0.65:
							positiveKpn += 1
						if result.max() == "Negative" and result.prob("Negative") >= 0.65:
							negativeKpn += 1
						counter += 1
					else:
						continue
				for item in KlmTriggers:
					if item in line.split():
						result = classifier.prob_classify(extract_features(line.split()))
						if result.max() == "Positive" and result.prob("Positive") >= 0.65:
							positiveKlm += 1
						if result.max() == "Negative" and result.prob("Negative") >= 0.65:
							negativeKlm += 1
						counter += 1
					else:
						continue
				for item in ShellTriggers:
					if item in line.split():
						result = classifier.prob_classify(extract_features(line.split()))
						#print(result.max(), result.prob(result.max()))
						if result.max() == "Positive" and result.prob("Positive") >= 0.65:
							positiveShell += 1
						if result.max() == "Negative" and result.prob("Negative") >= 0.65:
							negativeShell += 1
						counter += 1
					else:
						continue
				for item in INGTriggers:
					if item in line.split():
						result = classifier.prob_classify(extract_features(line.split()))
						if result.max() == "Positive" and result.prob("Positive") >= 0.65:
							positiveING += 1
						if result.max() == "Negative" and result.prob("Negative") >= 0.65:
							negativeING += 1
						counter += 1
					else:
						continue
						
		print("Datafile: {} PKPN: {} NKPN: {} PKLM: {} NKLM: {} PING: {} NING: {} PSHELL: {} NSHELL: {}".format(testfile, positiveKpn, negativeKpn, positiveKlm, negativeKlm, positiveING, negativeING, positiveShell, negativeShell))	
		
main()
