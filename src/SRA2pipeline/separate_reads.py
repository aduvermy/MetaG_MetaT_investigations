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

def process(lines=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}

try:
    fn = args.fastq
except IndexError as ie:
    raise SystemError("Error: Specify file name\n")

if not os.path.exists(fn):
    raise SystemError(f"Error: File {args.fastq} does not exist\n")





read_1 = open(f"{args.output}{base}_1.fastq","w")
read_2 = open(f"{args.output}{base}_2.fastq","w")



print("PROCESS READING AND WRITING FASTQ")

n = 4
with open(fn, 'r') as fh:
    lines = []
    for line in fh:
        lines.append(line.rstrip())
        if len(lines) == n:
            seqRecord = process(lines)
            #sys.stderr.write("Record: %s\n" % (str(record)))
            readID = seqRecord['name']
            splited = readID.split(" ")
            readID_1 = str(splited[0] + "/1")
            readID_2 = str(splited[0] + "/2")
            readSEQ_1 = seqRecord['sequence'][:125]
            readSEQ_2 = seqRecord['sequence'][125:]
            score_1 = seqRecord['quality'][:125]
            score_2 = seqRecord['quality'][125:]

            ### writing PE fastq
            read_1.write(f"{readID_1}\n")
            read_1.write(f"{readSEQ_1}\n")
            read_1.write("+\n")
            read_1.write(f"{score_1}\n")

            read_2.write(f"{readID_2}\n")
            read_2.write(f"{readSEQ_2}\n")
            read_2.write("+\n")
            read_2.write(f"{score_2}\n")
            
            #reset line        
            lines = []

print("END PROCESS\n")



read_1.close()
read_2.close()
