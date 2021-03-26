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
print(f"output : {args.output}{base}_interleaved.fastq \n" )
output_f = open(f"{args.output}{base}_interleaved.fastq","w")



def process(lines=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines)}

try:
    fn = args.fastq
except IndexError as ie:
    raise SystemError("Error: Specify file name\n")

if not os.path.exists(fn):
    raise SystemError(f"Error: File {args.fastq} does not exist\n")

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

            ### writing interleaved fastq
            output_f.write(f"{readID_1}\n")
            output_f.write(f"{readSEQ_1}\n")
            output_f.write("+\n")
            output_f.write(f"{score_1}\n")

            output_f.write(f"{readID_2}\n")
            output_f.write(f"{readSEQ_2}\n")
            output_f.write("+\n")
            output_f.write(f"{score_2}\n")
            
            #reset line        
            lines = []

print("END PROCESS\n")

output_f.close()