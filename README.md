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

# Useful Links
[structure Tara Ocean](http://ocean-microbiome.embl.de/companion.html)  
[prodigal Fast, reliable protein-coding gene prediction for prokaryotic genomes.](https://github.com/hyattpd/Prodigal)  
[Atlas](https://github.com/metagenome-atlas/atlas)  
[Metagenomic assembly tools](https://academic.oup.com/view-large/206266243)
