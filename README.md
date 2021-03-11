h # MetaG_MetaT_investigations
Metagenomic &amp; metatransciptomic coral reaf investigations

# CAMI

|   LOW   |   MEDIUM     |   HIGH      |
|:-------:|:------------:|:-----------:|
| Sample 1| Sample 1 5kbp|   sample 1  |


### ATLAS to AMBER

Convert fasta to csv  
```
./convert_bins.py -p ../../../RL/RL-S001--insert-270/binning/DASTool/bins/*maxbin*.fasta -s ../../../RL/RL-S001--insert-270/sequence_alignment/RL-S001--insert-270.sam -o ../../../AMBER/RL/maxbin_bins.tsv

./convert_bins.py -p ../../../RL/RL-S001--insert-270/binning/DASTool/bins/*metabat*.fasta -s ../../../RL/RL-S001--insert-270/sequence_alignment/RL-S001--insert-270.sam -o ../../../AMBER/RL/metabat_bins.tsv
```

From DASTool
```
./convert_bins.py -c ../../../RL/RL-S001--insert-270/binning/DASTool/cluster_attribution.csv -s ../../../RL/RL-S001--insert-270/sequence_alignment/RL-S001--insert-270.sam -o ../../../AMBER/RL/dastool_bins.tsv

```

Add column LENGTH to GS.bining
```
./add_column_length.py -s ../../../RL/data/RL.fastq -g ../../../AMBER/RL/gs_read_mapping.binning -o ../../../AMBER/RL/gs_read_mapping.binning.length
```

Add sample name (CAMI_low) on first line of files used by amber
```
sed -i '1 i\@Version:0.9.1\n@SampleID:CAMI_low\n\n' metabat_bins.tsv
sed -i '1 i\@Version:0.9.1\n@SampleID:CAMI_low\n\n' maxbin_bins.tsv
sed -i '1 i\@Version:0.9.1\n@SampleID:CAMI_low\n\n' gs_read_mapping.binning.length
```
amber  

``̀
amber.py -g gs_read_mapping.binning_strip --ncbi_nodes_file taxdump/nodes.dmp -o ./ maxbin_bins.tsv metabat_bins.tsv
``̀
Download taxdump.tar.gz from ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz, extract nodes.tmp, and provide it to AMBER with option --ncbi_nodes_file

## ATLAS binning observation

DAS Tool is an automated method that integrates a flexible number of binning algorithms to calculate an optimized, non-redundant set of bins from a single assembly. We show that this approach generates a larger number of high-quality genomes than achieved using any single tool.
In ATLAS pipeline DAS Tool merge information from metatabat and maxbin.

### LOW

<img src="./issues/atlas_binning/compl_purity_low.png">

<img src="./issues/atlas_binning/contamin_low.png">


### HIGH

<img src="./issues/atlas_binning/compl_purity_high.png">

<img src="./issues/atlas_binning/contamin_high.png">


# Public datasets

### Metagenomic seawater

|   SRX7913443                            |   SPRJNA329908      |      PRJEB22493            |
|:---------------------------------------:|:-------------------:|:-----------------------------:|
|           1                             |               329   |         495                   |
|shotgun sequencing of sediment sample D18| seawater metagenome | reference alignment + assembly|


### Coral reaf metagenomic

|   PRJNA357506                           |   PRJEB28183        |       mgp81589                |
|:---------------------------------------:|:-------------------:|:-----------------------------:|
|           16                            |               689   |         26                    |
|impact of aquaculture effluent on Red Sea coral reef water nutrients and microorganisms| Coral-associated bacteria demonstrate phylosymbiosis and cophylogeny | rMicrobiome of Pseudodiploria strigosa across Bermuda's reefs|

### Metatranscriptomic

|   SRX4803467                            |               SRX6899989                         |  
|:---------------------------------------:|:------------------------------------------------:|
|           1                             |               1                                  |
|Antarctic marine metatranscriptome       | Metatranscriptomic data from Coast of New Jersey |

# Metagenomic

## Atlas workflow

<img src="./issues/ATLAS_scheme.png">

## Sunbeam workflow

<img src="./issues/SUNBEAM_scheme.png">

## mOTU2 an alternative for taxonomic assignation

<img src="./issues/mOTU.png">

## Comparison between workflow

<img src="./issues/table_comparison.png">

# Metatranscriptomic

## Metatrans workflow

<img src="./issues/metatrans.jpeg">

## Samsa2 workflow

<img src="./issues/samsa2.jpg">







# Useful Links
[structure Tara Ocean](http://ocean-microbiome.embl.de/companion.html)  
[prodigal Fast, reliable protein-coding gene prediction for prokaryotic genomes.](https://github.com/hyattpd/Prodigal)  
[Atlas](https://github.com/metagenome-atlas/atlas)  
[Metagenomic assembly tools](https://academic.oup.com/view-large/206266243)
