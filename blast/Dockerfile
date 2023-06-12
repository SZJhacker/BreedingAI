FROM wurmlab/sequenceserver:1.0.11
COPY IRGSP-1.0_genome.fasta.gz /db/IRGSP-1.0_genome.fasta.gz
WORKDIR /db
RUN gunzip IRGSP-1.0_genome.fasta.gz 
RUN sequenceserver -m -d ./ 
