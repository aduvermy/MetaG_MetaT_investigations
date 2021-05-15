#!/usr/bin/env python3
import pandas as pd
import io
#import requests
from ete3 import NCBITaxa
import argparse



parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--diamond_tsv','-d', type=str,
                    help='Path of humann diamond tsv file. For exemple : "hard_filtered_transcripts_diamond_aligned.tsv" ')
parser.add_argument('--output', '-o', type=str,
                    help='output file tsv :  "SRR74_taxo.tsv"')


args = parser.parse_args()



##request fonction
def get_desired_ranks(taxid, desired_ranks):
    lineage = ncbi.get_lineage(taxid)   
    names = ncbi.get_taxid_translator(lineage)
    lineage2ranks = ncbi.get_rank(names)
    ranks2lineage = dict((rank,taxid) for (taxid, rank) in lineage2ranks.items())
    return{'{}_id'.format(rank): ranks2lineage.get(rank, '<not present>') for rank in desired_ranks}




diamond_file = args.diamond_tsv

print("PROCESS READING diamond file")
diamond_dtf = pd.read_csv(diamond_file, sep= '\t', header = None)

#print(diamond_dtf.groupby([0,10])[10].min())
index_uniq = diamond_dtf.groupby([0])[10].idxmin()

diamond_dtf_filtered = diamond_dtf.iloc[index_uniq,:]

dta = diamond_dtf_filtered
print('READING DONE\n\n')


print('REQUEST UNIPROT AND NCBI')
dict_taxo={}
for index, row in diamond_dtf_filtered.iterrows():
    uniref_id = row[1].split('|')[0]
    #print(dta.iloc[row,10])

    url = f"https://www.uniprot.org/uniref/{uniref_id}.tab"
    try :
        df = pd.read_csv(url, sep ='\t')
    except:
        try:
            uniref_id = uniref_id.split('_')[1]
            url = f"https://www.uniprot.org/uniref/uniref100_{uniref_id}.tab"
            df = pd.read_csv(url, sep ='\t')
        except:
            print(f'issue with {uniref_id}')
            continue

    ncbi = NCBITaxa()
    protein = df['Protein names'].values[0]
    contig  = row[0]
    taxids = df['Organism IDs']
    desired_ranks = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    for taxid in taxids:
        #print(list(ncbi.get_taxid_translator([taxid]).values())[0])
        ranks = get_desired_ranks(taxid, desired_ranks)
        sub_dict = {}
        for key, rank in ranks.items():
            if rank != '<not present>':
            #    print(key + ': ' + list(ncbi.get_taxid_translator([rank]).values())[0])
            #print(key)
                sub_dict[key] = list(ncbi.get_taxid_translator([rank]).values())[0]
            else:
                sub_dict[key] = "NA"
            sub_dict['taxid'] = taxid
            sub_dict['unirefid'] = uniref_id
            sub_dict["protein"]=protein
            dict_taxo[contig] = sub_dict

#print(dict_taxo.keys())
#print(dict_taxo)
taxo_dtaF = pd.DataFrame(dict_taxo).T
#taxo_dtaF['Contigs'] = taxo_dtaF.index
taxo_dtaF = taxo_dtaF.reset_index()
print('request done')



print('writing results')
taxo_dtaF.to_csv(args.output, index=False, sep = '\t')
print('END')