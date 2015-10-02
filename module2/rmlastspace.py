import sys

file = open(sys.argv[1], "r")
data = file.readlines()
file.close()
file = open(sys.argv[1], "w")
for line in data:
	line = line[0:len(line) - 1]
	file.write(line)
	file.write("\n")