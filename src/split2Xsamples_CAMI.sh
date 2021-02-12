R1=$1
R2=$2
K=3

split -N $K $R1 ${R1%.*}_part
split -N $K $R2 ${R2%.*}_part
