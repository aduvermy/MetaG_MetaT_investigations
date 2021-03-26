#!/usr/bin/env python3

import os
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
import pandas as pd

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--read2genome','-r', type=str,
                    help='Path of reads2genome file. For exemple : "reads2genome.tsv" ')
parser.add_argument('--genome2taxonomy', '-t', type=str,
                    help='Path of taxonomy file :  "gtdbtk.bac120.summary.tsv"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "input_krona.tsv"')

args = parser.parse_args()

print("PROCESS READING reads2genome")
try:
    read2genome = pd.read_csv(args.read2genome, sep='\t', header=None)
except:
    print(f"ERROR with {args.read2genome}\n\n")
    exit()
read2genome.columns = [ "READ", "TAXID" ] #rename column
print("END PROCESS\n")


print("PROCESS READING taxonomy")
try:
    genome2taxo = pd.read_csv(args.genome2taxonomy, sep='\t')
except:
    print(f"ERROR with {args.genome2taxonomy}\n\n")
    exit()
print("END PROCESS\n")


print("PROCESS WRITING OUTPUT")
taxonomy = genome2taxo.sort_values("user_genome").classification.tolist()
abondance = read2genome.TAXID.value_counts().rename_axis('MAG').reset_index(name='counts').sort_values("MAG")

with open(args.output, 'w') as f:
    for i in range(len(taxonomy)):
        taxo = taxonomy[i].strip('s__').split(';')
        taxo_cleaned = list(filter(None, taxo))
        taxo_cleaned = '\t'.join(map(str, taxo_cleaned))
        f.write(f"{abondance.counts[i]}\t{taxo_cleaned}\n")
print("END PROCESS\n")