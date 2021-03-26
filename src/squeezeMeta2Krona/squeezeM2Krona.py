#!/usr/bin/env python3

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Check my input')


parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "squeeze.taxonomy"')
parser.add_argument('--taxonomy', '-t', type=str,
                    help='Path of mcount file. For exemple :  "results/11.CAMI_high.mcount"')


args = parser.parse_args()


print("PROCESS READING 11.SAMPLE.mcount")
try:
    taxo_counts = pd.read_csv(args.taxonomy, sep='\t').dropna()
except:
    print(f"ERROR with {args.taxonomy}\n\n")
    exit()
print("END PROCESS\n")


print("PROCESS WRITING OUTPUT")
taxonomy = taxo_counts.Taxon.tolist()
abondance = taxo_counts["CAMI_high reads"].tolist()

with open(args.output, 'w') as f:
    for i in range(len(taxonomy)):
        taxo = taxonomy[i].split(';')
        taxo_cleaned = list(filter(None, taxo))
        taxo_cleaned = '\t'.join(map(str, taxo_cleaned))
        #print(taxo_cleaned)
        f.write(f"{int(abondance[i])}\t{taxo_cleaned}\n")
print("END PROCESS\n")