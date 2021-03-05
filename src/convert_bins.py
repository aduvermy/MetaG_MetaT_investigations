#!/usr/bin/env python3

import os
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
import pandas as pd

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--pattern2Bins','-p', type=argparse.FileType('r'), nargs='+',
                    help='Path of bins inferred from contigs. For exemple : "binning/*.metabat*.fasta" ')
parser.add_argument('--samFile', '-s', type=str,
                    help='Path of sam file. For exemple :  "sequence_alignment/mysample.sam"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "metabat_bins.tsv"')

args = parser.parse_args()

print("PROCESS READING BINS FILES")
##Build dict with contig as key and bin file as value
binsContig = dict()
try:
    #Ouverture des bins
    pattern2bins = args.pattern2Bins
    for f in pattern2bins:
        for contig, sequence in SimpleFastaParser(f):
            binsContig[contig]=os.path.basename(f.name)


except:
    print(f"ERROR with {f.name}\n\n")
print("END PROCESS\n")





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
    len_reads = len(line[9])
    if contigID in binsContig:
        binsReads[readID]= [ binsContig[contigID], len_reads ] #contig unknown (metabat/maxbin)
    else:
        continue
print("END PROCESS\n")

print("PROCESS BUILDING TSV")
mybin = pd.DataFrame(list(binsReads.items()), columns=['@@SEQUENCEID', 'BINID'])
mybin_tmp = pd.DataFrame(mybin.BINID.tolist(), index= mybin.index, columns=['BINID', '_LENGTH'])
mybin = pd.concat([mybin['@@SEQUENCEID'], mybin_tmp], axis=1)
mybin.to_csv(args.output, sep="\t", index=False)
print("END PROCESS\n")
