path2CAMI = $1
outputfile = ${path2CAMI%.*}


cat  $path2CAMI | grep '^@.*/1$' -A 3 --no-group-separator > ${outputfile}_1.fastq
cat $path2CAMI | grep '^@.*/2$' -A 3 --no-group-separator > ${outputfile}_2.fastq
