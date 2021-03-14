# MetaG_MetaT_investigations
Metagenomic &amp; metatransciptomic coral reaf investigations

# CAMI

|   LOW   |   MEDIUM     |   HIGH      |
|:-------:|:------------:|:-----------:|
| Sample 1| Sample 1 5kbp|   sample 1  |


## Atlas trouble with medium 

    -> Possibly linked to insert size and mate-pair library 

[Paired-end read confusion - library, fragment or insert size?](http://thegenomefactory.blogspot.com/2013/08/paired-end-read-confusion-library.html)

[Using Velvet with mate-pair sequences](http://thegenomefactory.blogspot.com/2012/09/using-velvet-with-mate-pair-sequences.html)

Mate-pair reads are extremely valuable in a de novo setting as they provide long-range information about the genome, and can help link contigs together into larger scaffolds. They have been used reliably for years on the 454 FLX platform, but used less often on the Illumina platform. I think the main reasons for this are the poorer reliability of the Illumina mate-pair protocol and the larger amount of DNA required compared to a PE library.

We can consider MP reads as the same as PE reads, but with a larger distance between them ("insert size"). But there is one technical difference due to the circularization procedure used in their preparation. PE reads are oriented "opp-in" (L=>.....<=R), whereas MP reads are oriented "opp-out" (L<=.....=>R).

<img src="./issues/insert_sch.png"> 

Note that in order to use SPAdes 3.1+ for mate-pair only assemblies you need to have the so-called "high quality mate pairs". Right now such mate pairs can only be generated using Nextera mate pair protocol. Everything else would give you suboptimal assemblies.
[MP and SPADE](https://www.biostars.org/p/111202/)

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

``` 
amber.py -g gs_read_mapping.binning_strip --ncbi_nodes_file taxdump/nodes.dmp -o ./ maxbin_bins.tsv metabat_bins.tsv
```   
Download taxdump.tar.gz from ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz, extract nodes.tmp, and provide it to AMBER with option --ncbi_nodes_file

## ATLAS assembly evaluation 

Possible choice between spade and megahit for assembly




## ATLAS binning evaluation

DAS Tool is an automated method that integrates a flexible number of binning algorithms to calculate an optimized, non-redundant set of bins from a single assembly. We show that this approach generates a larger number of high-quality genomes than achieved using any single tool.
In ATLAS pipeline DAS Tool merge results from Metatabat and Maxbin.

**N.B: Recall = completeness, precision = purity**

LOW                        |  HIGH
:-------------------------:|:-------------------------:
<img src="./issues/atlas_binning/compl_purity_low.png">  |  <img src="./issues/atlas_binning/compl_purity_high.png">
<img src="./issues/atlas_binning/contamin_low.png"> |   <img src="./issues/atlas_binning/contamin_high.png">



We observe that Maxbin is quite better than Metabat on low complexity samples. But Metabat  worked much better once applied to high complexity dataset.
By merging Metabat and Maxbin results, DAS Tool improves the completeness of the bins. 
/!\ On a low complexity dataset, the completeness of bins is maximized but the contamination is increased too.





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
