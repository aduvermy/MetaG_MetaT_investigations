#!/usr/bin/env python3

import os
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
import pandas as pd

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--samFile', '-s', type=str,
                    help='Path of sam file. For exemple :  "sequence_alignment/mysample.sam"')
parser.add_argument('--goldStandard', '-g', type=str,
                    help='Path of sam file. For exemple :  "gs_read_mapping.bining"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "gs_read_mapping.bining.length"')

args = parser.parse_args()


print("PROCESS READING GS")
try:
    gs = pd.read_csv(args.goldStandard, sep='\t', comment='@' )
except:
    print(f"ERROR with {args.goldStandard}\n\n")
    exit()
gs.columns = [ '@@SEQUENCEID', 'BINID', 'TAXID', '_READID' ] #rename column
gs = gs.drop(['TAXID', '_READID'], axis = 1 ) #drop useless column
print("END PROCESS\n")


print("PROCESS READING SAM")
reads = dict()
#Build TSV bins with seqID == readID
try:
    samF = open(args.samFile, 'r')
except:
    print(f"ERROR with {args.samFile}\n\n")
    exit()

for line in samF:
    if line[0]=="@":
        continue
    line=line.strip().split('\t')
    readID = line[0]
    len_reads = len(line[9])
    reads[readID] = len_reads
print("END PROCESS\n")

print("PROCESS READING SAM")
reads_len = pd.DataFrame(list(reads.items()), columns=['@@SEQUENCEID', '_LENGTH'])
#print(pd.concat([gs, reads_len['_LENGTH']] , axis=1, join='inner'))
gs_final = gs.merge(reads_len, on= "@@SEQUENCEID")
gs_final.to_csv(args.output, sep="\t", index=False)
print("END PROCESS\n")
