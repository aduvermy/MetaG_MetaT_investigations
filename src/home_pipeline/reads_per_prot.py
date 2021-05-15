#!/usr/bin/env python3

import os
import argparse

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--reads_contigs', '-c', type=str,
                    help='Path of reads per contig tsv file. For exemple :  "SRR74_reads_per_contig.tsv"')
parser.add_argument('--diamond', '-d', type=str,
                    help='Path of diamond taxa output. For exemple :  "SRR_taxa.tsv"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "transcript_per_prot.tsv"')


args = parser.parse_args()



print("PROCESS READING diamond res")
protDict = dict()
#Build TSV bins with seqID == readID

try:
    diamond = open(args.diamond, 'r')
except:
    print(f"ERROR with {args.diamond}\n\n")
    exit()

diamond.readline() #skip header
for line in diamond:
    line = line.strip().split('\t')
    contigID = line[0]
    protID = line[3]
    if contigID in protDict:
        print(contigID)
        print('contigID with multiple assignation')
        exit()
    else:
        protDict[contigID] = protID   
print("END PROCESS\n")



print("PROCESS READING reads per contig")
readsDict = dict()
#Build TSV bins with seqID == readID

try:
    reads_contig = open(args.reads_contigs, 'r')
except:
    print(f"ERROR with {args.reads_contig}\n\n")
    exit()

for line in reads_contig:
    line = line.strip().split('\t')
    contigID = line[0]
    readsNB = line[1]
    if contigID in readsDict:
        print('contigID repeat in file')
        exit()
    else:
        readsDict[contigID] = readsNB   
print("END PROCESS\n")



print('WRITING OUTPUT')
outputDict= {}
for contigID in protDict:
    prot = protDict[contigID]
    try :
        sub_count = int(readsDict[contigID])
    except:
        print(f"no reads mapped in {contigID}")
        continue
    #print(sub_count)
    if prot in outputDict:
        outputDict[prot] =+ sub_count
    else:
        outputDict[prot]= sub_count

o = open(args.output, 'w')
for prot in outputDict:
    count = outputDict[prot]
    o.write(f"\n{prot}\t{count}")
print('end')