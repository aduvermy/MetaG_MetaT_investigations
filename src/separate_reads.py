#!/usr/bin/env python3

import os
import sys

basename = os.path.basename(sys.argv[1])
splited_base = basename.split(".")
base = splited_base[0]


read_1 = open(base+"_1.fastq","w")
read_2 = open(base+"_2.fastq","w")

with open(sys.argv[1], "r") as f:
	for line in f:
		if "@SRR" == line[:3] or "+SRR" == line[:3]:
			splited = line.split(" ")
			read_1.write(splited[0] + "/1")
			read_2.write(splited[0] + "/2")
		else:
			read_1.write(line[:125]+ "\n")
			read_2.write(line[125:]+ "\n")

read_1.close()
read_2.close()
