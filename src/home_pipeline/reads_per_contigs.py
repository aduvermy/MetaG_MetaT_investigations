#!/usr/bin/env python3

import os
import argparse

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--sam', '-s', type=str,
                    help='Path of tsv. For exemple :  "SRR74.sam"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "reads_per_contig.tsv"')


args = parser.parse_args()



print("PROCESS READING SAM")
contigDict = dict()
#Build TSV bins with seqID == readID

try:
    sam = open(args.sam, 'r')
except:
    print(f"ERROR with {args.sam}\n\n")
    exit()


for line in sam:
    if line[0]=="@":
        continue
    line=line.strip().split('\t')
    contigID = line[2]
    if contigID in contigDict:
        contigDict[contigID] +=1
    else:
        contigDict[contigID] = 1
print("END PROCESS\n")


print('WRITING OUTPUT')
o = open(args.output, 'w')
o.write(f"key\tread_count")
for key in contigDict:
    count = contigDict[key]
    o.write(f"\n{key}\t{count}")
print('end')