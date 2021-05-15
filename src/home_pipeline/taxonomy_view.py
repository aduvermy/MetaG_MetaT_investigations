#!/usr/bin/env python3


import os
import argparse

parser = argparse.ArgumentParser(description='Check my input')


parser.add_argument('--reads_contigs', '-c', type=str,
                    help='Path of reads per contig tsv file. For exemple :  "SRR74_reads_per_contig.tsv"')
parser.add_argument('--diamond', '-d', type=str,
                    help='Path of tsv. For exemple :  "SRR77_metaT_taxo.tsv"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "taxa_view.tsv"')


args = parser.parse_args()



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





print("PROCESS READING diamond res")
classDict = dict()
kingdomDict = dict()
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
    classID = line[6]
    kingdomID= line[5]
    if classID in classDict:
        #print(classID)
        classDict[classID] += int(readsDict[contigID])
    else:
        classDict[classID] = int(readsDict[contigID])

    if kingdomID in kingdomDict:
        kingdomDict[kingdomID] += int(readsDict[contigID])
    else:
        kingdomDict[kingdomID] = int(readsDict[contigID])
print("END PROCESS\n")

print('WRITING OUTPUT')
o_k = open(f"{args.output}_kindom", 'w')
o_k.write(f"kingdom\tread_count")

o_c = open(f"{args.output}_class", 'w')
o_c.write(f"class\tread_count")
print(classDict)
for key in kingdomDict:
    count = kingdomDict[key]
    o_k.write(f"\n{key}\t{count}")

for key in classDict:
    count = classDict[key]
    o_c.write(f"\n{key}\t{count}")

print('end')