# MetaG_MetaT_investigations
Metagenomic &amp; metatransciptomic coral reaf investigations

# Install nextflow

```
cd MetaG_MetaT_investigations
curl -s https://get.nextflow.io | bash
```
# Launch Pipeline

```
./nextflow run src/metaG_analysis.nf -c src/metaG_analysis.config -profile pedago --inputFromSRA SRR5113072 -resume
```

# CAMI

|   LOW   |   MEDIUM     |   HIGH      |
|:-------:|:------------:|:-----------:|
| Sample 1| Sample 1 5kbp|   sample 1  |

# Public datasets

### Metagenomic seawater

|   SRX7913443                            |   SPRJNA329908      |       PRJEB22493              |
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


# Atlas workflow

<img src="./issues/ATLAS_scheme.png">

# Sunbeam workflow

<img src="./issues/SUNBEAM_scheme.png">

# mOTU2 workflow

<img src="./issues/mOTU.png">

# Comparison

<img src="./issues/table_comparison.png">





# Useful Links
[structure Tara Ocean](http://ocean-microbiome.embl.de/companion.html)  
[prodigal Fast, reliable protein-coding gene prediction for prokaryotic genomes.](https://github.com/hyattpd/Prodigal)  
[Atlas](https://github.com/metagenome-atlas/atlas)  
[Metagenomic assembly tools](https://academic.oup.com/view-large/206266243)
