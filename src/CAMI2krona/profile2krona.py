#!/usr/bin/env python3


import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--profile', '-p', type=str,
                    help='Path of fastq file. For exemple :  "sequence_alignment/mysample.fastq"')
parser.add_argument('--goldStandard', '-g', type=str,
                    help='Path of goldStandard file. For exemple :  "gs_read_mapping.bining"')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "krona.tsv')

args = parser.parse_args()

print("PROCESS READING GS")
try:
    gs = pd.read_csv(args.goldStandard, sep='\t', comment='@', header=None )
except:
    print(f"ERROR with {args.goldStandard}\n\n")
    exit()
gs.columns = [ '@@SEQUENCEID', 'BINID', 'TAXID', '_READID' ] #rename column
#gs = gs.drop(['TAXID', '_READID'], axis = 1 ) #drop useless column
print("END PROCESS\n")


print("PROCESS READING profile")
try:
    profile = pd.read_csv(args.profile, sep='\t', comment='@' , header = None)
except:
    print(f"ERROR with {args.profile}\n\n")
    exit()
profile.columns = [ "TAXID","RANK","TAXPATH","TAXPATHSN","PERCENTAGE","_CAMI_genomeID","_CAMI_OTU" ] #rename column
#gs = gs.drop(['TAXID', '_READID'], axis = 1 ) #drop useless column
print("END PROCESS\n")


#print(gs)
print("PROCESS BUILDING TAXONOMY KRONA")

abondance = gs.TAXID.value_counts().rename_axis('TAXID').reset_index(name='counts')
abondance_taxo = pd.merge(abondance, profile, how='inner', on=['TAXID', 'TAXID'])
taxonomy = abondance_taxo.TAXPATHSN.str.split("|")

print("END PROCESS\n")

print("PROCESS WRITING KRONA FILE")

with open(args.output, 'w') as f:
    for i in range(len(taxonomy)):
        taxo_cleaned = list(filter(None, taxonomy[i]))
        taxo_cleaned = '\t'.join(map(str, taxo_cleaned))
        #print(abondance_taxo.counts[i])
        f.write(f"{abondance_taxo.counts[i]}\t{taxo_cleaned}\n")
print("END PROCESS\n")
