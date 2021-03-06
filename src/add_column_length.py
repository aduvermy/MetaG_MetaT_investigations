#!/usr/bin/env python3

import os
import argparse
from Bio import SeqIO
import pandas as pd

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--fastq', '-f', type=str,
                    help='Path of fastq file. For exemple :  "sequence_alignment/mysample.fastq"')
parser.add_argument('--goldStandard', '-g', type=str,
                    help='Path of goldStandard file. For exemple :  "gs_read_mapping.bining"')
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


print("PROCESS READING FASTQ")
reads = dict()

for seqRecord in SeqIO.parse(args.fastq, "fastq"):
       len_reads = len(seqRecord.seq)
       readID = seqRecord.id[:-2]
       reads[readID] = len_reads
print("END PROCESS\n")




print("PROCESS WRITING GS WITH COL LENGTH")
reads_len = pd.DataFrame(list(reads.items()), columns=['@@SEQUENCEID', '_LENGTH'])
#print(pd.concat([gs, reads_len['_LENGTH']] , axis=1, join='inner'))
gs_final = gs.merge(reads_len, on= "@@SEQUENCEID")
print(gs_final)
gs_final.to_csv(args.output, sep="\t", index=False)
print("END PROCESS\n")
