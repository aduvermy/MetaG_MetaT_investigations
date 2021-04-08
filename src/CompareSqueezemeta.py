import os
import argparse
from Bio.SeqIO.FastaIO import SimpleFastaParser
import pandas as pd

parser = argparse.ArgumentParser(description='Check my input')

parser.add_argument('--goldStandard','-g', type=str,
 					help='Path of goldstandard for exemple : "CAMI/*medium_complexity*.profile" ')
parser.add_argument('--profileResults', '-p', type=str,
					help='Path of profile file. For exemple :  ')
parser.add_argument('--numberReadsGold', '-n', type=int,
					help='Path of profile file. For exemple :  ')

args = parser.parse_args()

def ifkeyin(key, dic, type_dic):
	if key in dic:
		return dic
	else:
		if type_dic == 0:
			dic[key] = {}
		else:
			dic[key] = []
		return dic

def min_read(min_reads, number_of_reads):
	if int(min_reads) > int(number_of_reads):
		return number_of_reads
	else:
		return min_reads


print("PROCESS READING GOLDSTANDARD")
##Build dict with contig as key and bin file as value
profileGold = dict()
dic_clad = dict()
try:

	goldStandard = open(args.goldStandard, "r")



except:
	print(f"ERROR with goldstandard\n\n")
	print("END PROCESS\n")

try:

	nb_reads = args.numberReadsGold



except:
	print(f"ERROR with numberReadsGold\n\n")
	print("END PROCESS\n")

numberSpeciesGold = 0
min_read_gold =  nb_reads
for line in goldStandard:
	if line[0] == "@" or line[0] == "\n":
		continue
	else:
		split_tab = line.split("\t")
		taxa = split_tab[3].split("|")
		number_of_reads = float(split_tab[4]) * nb_reads 
		min_read(min_read_gold, number_of_reads)
		if "Viruses" == taxa[0]:
			pass
		else:
			profileGold = ifkeyin(taxa[-1].lower(), profileGold, 0)
			dic_clad = ifkeyin(split_tab[1], dic_clad, 1)
			dic_clad[split_tab[1]].append(taxa[-1].lower())
			profileGold[taxa[-1].lower()]["order"] = split_tab[1]
			profileGold[taxa[-1].lower()]["name"] = taxa[-1].lower()
			profileGold[taxa[-1].lower()]["percent"] =  number_of_reads
			profileGold[taxa[-1].lower()]["profile_obtained"] = 0
			numberSpeciesGold  += 1


goldStandard.close()

dic_not_in_gold = {}
numberSpeciesProfile = 0
average_error = 0
number_Fragment_Result = 0
number_of_fragments_False = 0
number_of_fragments_False_not_pass =0
dic_not_in = {}
try:

	profileResults = open(args.profileResults, "r")



except:
	print(f"ERROR with profile Results \n\n")
	print("END PROCESS\n")


for line in profileResults:
	if line[0:4] == "Rank" or line[0] == "\n":
		continue
	else:
		split_tab = line.split("\t")
		taxa_profil = split_tab[1].split(";")
		if split_tab[0] == "k":
			number_Fragment_Result += int(split_tab[3])
		if taxa_profil[-1][2:].lower() in profileGold:
			profileGold[taxa_profil[-1][2:].lower()]["profile_obtained"] = 1
			gold_read =  profileGold[taxa_profil[-1][2:].lower()]["percent"]
			profileGold[taxa_profil[-1][2:].lower()]["percent"] =  abs((int(split_tab[3]) - gold_read))/nb_reads
			average_error += float(profileGold[taxa_profil[-1][2:].lower()]["percent"])
			numberSpeciesProfile += 1 

		else:
			if split_tab[3] == "":
				split_tab[3] = 0
			dic_not_in = ifkeyin(split_tab[0], dic_not_in, 0)
			dic_not_in[split_tab[0]][taxa_profil[-1][2:]] = int(split_tab[3])
			print(min_read_gold)
			if int(split_tab[3]) <  int(min_read_gold) : 
				number_of_fragments_False_not_pass += int(split_tab[3])
				pass
			else:
				
				number_of_fragments_False += int(split_tab[3])
print(number_of_fragments_False_not_pass)

profileResults.close()

###Metrics###

percent_found = numberSpeciesProfile*100/numberSpeciesGold
percent_wrong_taxa = (number_of_fragments_False + number_of_fragments_False_not_pass)*100/ number_Fragment_Result
percent_wrong_taxa_up_threshold = number_of_fragments_False*100 / number_Fragment_Result
average_error = 0
total_found = 0
with open("summary_squeezemeta_read.txt", "w") as output:
	
	for clade in dic_clad.keys():
		found = 0
		percent_error = 0
		total = len(dic_clad[clade])
		for taxid in  dic_clad[clade]:
			if profileGold[taxid]["profile_obtained"] == 1:
				found += 1 
				percent_error += float(profileGold[taxid]["percent"])
				total_found += 1
				average_error += float(profileGold[taxid]["percent"])
		if found == 0:
			percent_error = "none found"
		else:
			percent_error = percent_error/ found
			
		found_percent = found*100 / total 
		output.write("Statistics on {} \n\n".format(clade)) 
		output.write("Percent of {}  found : {} \n".format(clade, found_percent))
		output.write("percentage of error : {} \n".format(percent_error))
	average_error = average_error / total_found 
	output.write("\n \n percent of total taxa found : {}  \n average error in percent : {} \n percent of reads assigned to non present taxa {}\n".format(percent_found, average_error, percent_wrong_taxa))
	output.write("percent of non existing taxa passing the threshold : {} \n".format(percent_wrong_taxa_up_threshold))