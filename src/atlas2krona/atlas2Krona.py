#!/usr/bin/env python3

import os
import argparse
import pandas as pd
import subprocess


parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--read2genome','-r', type=str,
                    help='Path of raw_counts_genome.tsv file. For exemple : "raw_counts_genome.tsv" ')
parser.add_argument('--genome2taxonomy', '-t', type=str,
                    help='Path of taxonomy file :  "gtdbtk.bac120.summary.tsv"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "input_krona.tsv"')
parser.add_argument('--unmapped', '-u', type=str,
                    help='unmapped directory with end /:  "alignment/unmaped/"')

args = parser.parse_args()


print("PROCESS COUNTING NO HITS")
try:
    cmd = f"zcat {args.unmapped}* | grep -c '@R'"
    nohits = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode().strip()
except:
    print(f"ERROR with {args.unmaped}\n\n")
    exit()
print("END PROCESS\n")



print("PROCESS READING raw_counts_genome.tsv")
try:
    read2genome = pd.read_csv(args.read2genome, sep='\t')
except:
    print(f"ERROR with {args.read2genome}\n\n")
    exit()
read2genome.columns = [ "MAG", "NB_reads" ] #rename column
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
abondance = read2genome.sort_values("MAG").NB_reads.tolist()

with open(args.output, 'w') as f:
    f.write(f"{nohits}\tnoHITS\n")
    for i in range(len(taxonomy)):
        taxo = taxonomy[i].strip('s__').split(';')
        taxo_cleaned = list(filter(None, taxo))
        taxo_cleaned = '\t'.join(map(str, taxo_cleaned))
        f.write(f"{abondance[i]}\t{taxo_cleaned}\n")
print("END PROCESS\n")