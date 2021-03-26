#!/usr/bin/env python3

import os
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--samFile', '-s', type=str,
                    help='Path of sam file. For exemple :  "sequence_alignment/mysample.sam"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "metabat_bins.tsv"')
parser.add_argument('--contig2genome', '-g', type=str,
                    help='Path of fastq file. For exemple :  "genome/clustering/contig2genome.tsv"')


args = parser.parse_args()


print("PROCESS READING SAM")
binsReads = dict()
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
    contigID = line[2]
    binsReads[readID] = contigID
print("END PROCESS\n")


print("PROCESS READING contig2genome.tsv")
try:
    contig2genome = pd.read_csv(args.contig2genome, sep='\t', header=None)
except:
    print(f"ERROR with {args.contig2genome}\n\n")
    exit()
contig2genome.columns = [ "CONTIGID", "MAG" ] #rename column
print("END PROCESS\n")


print("PROCESS Wrting reads2MAG.tsv")
mybin = pd.DataFrame(list(binsReads.items()), columns=['READID', 'CONTIGID'])
#print(mybin.head(3))

#print("\n\n")
#print(contig2genome.head(3))
#print(mybin.shape)
#mybin = mybin[mybin['BINID'].astype(bool)]  
#mybin.BINID.replace('', np.nan, inplace=True)
#mybin.dropna(subset=['BINID'], inplace=True)
#mybin = pd.concat([mybin['READID'], contig2genome["MAG"] ], axis=1)

taxo_final = pd.merge(contig2genome, mybin , on="CONTIGID", how="outer", validate="one_to_many")
# taxo_final = mybin.merge(contig2genome, on= "CONTIGID")
taxo_final.drop('CONTIGID', inplace=True, axis=1)
#print(taxo_final.head(10))
taxo_final[["READID","MAG"]].to_csv(args.output, sep="\t", index=False, header=None)
print("END PROCESS\n")

