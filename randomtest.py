import random

def main():
	
	random.seed(4242)
	counter = 0
	bpos = open('Training/Positive/posfile_balanced.txt', 'w')
	with open('Training/Positive/posfile.txt', 'r') as pos:
		lines = random.sample(pos.readlines(),15090)
		for line in lines:
			bpos.write(line)
			
		
main()
