#!/usr/bin/env python3

import os
import argparse

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--tsv', '-t', type=str,
                    help='Path of tsv. For exemple :  "SRR74_prot2taxo.tsv"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "transcript_per_prot.tsv"')


args = parser.parse_args()



print("PROCESS READING TSV")
protDict = dict()
#Build TSV bins with seqID == readID

try:
    tsv = open(args.tsv, 'r')
except:
    print(f"ERROR with {args.tsv}\n\n")
    exit()


for line in tsv:
    line=line.strip().split('\t')
    protID = line[3]
    if protID in protDict:
        protDict[protID] +=1
    else:
        protDict[protID] = 1
print("END PROCESS\n")


print('WRITING OUTPUT')
o = open(args.output, 'w')
for key in protDict:
    count = protDict[key]
    o.write(f"\n{key}\t{count}")
print('end')