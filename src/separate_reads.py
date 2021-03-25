#!/usr/bin/env python3

import os
import argparse
from Bio import SeqIO
import pandas as pd


parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--fastq', '-f', type=str,
                    help='Path of fastq file. For exemple :  "sequence_alignment/mysample.fastq"')
parser.add_argument('--output', '-o', type=str,
                    help='output directory :  "../../"')

args = parser.parse_args()


basename = os.path.basename(args.fastq)
splited_base = basename.split(".")
base = splited_base[0]
print(f"output read 1: {args.output}{base}_1.fastq \n" )
print(f"output read 2: {args.output}{base}_2.fastq \n" )


read_1 = open(f"{args.output}{base}_1.fastq","w")
read_2 = open(f"{args.output}{base}_2.fastq","w")



with open(args.fastq, "r") as f:
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
