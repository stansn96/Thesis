def main():
	kpn, klm, ing, shell = 0, 0, 0, 0
	lines_seen = set() # holds lines already seen
	outfile = open("companies_18_new.txt", "w")
	for line in open("companyfile_18_new.txt", "r"):
		if line not in lines_seen: # not a duplicate
			outfile.write(line)
			lines_seen.add(line)
			for word in line.split():
				if word == 'kpn' or word == '#kpn':
					kpn += 1
					break
				elif word == 'klm' or word == '#klm' or word == 'france-klm' or word == 'airfrance-klm' or word == 'airfranceklm' or word == '#airfranceklm':
					klm += 1
					break
				elif word == 'ing' or word == '#ing':
					ing += 1
					break
				elif word == 'shell' or word == '#shell':
					shell += 1
					break
	outfile.close()
	print("KPN:", kpn)
	print("KLM:", klm)
	print("ING:", ing)
	print("Shell:", shell)
	print("Totaal:", kpn + klm + ing + shell)
	
main()
