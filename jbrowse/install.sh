gzip -d /jbrowse2/IRGSP-1.0_genome.fasta.gz 
tar -zxvf /jbrowse2/IRGSP-1.0_representative_2021-05-10.tar.gz
# tar -zxvf /jbrowse2/IRGSP-1.0_representative_2021-05-10.tar.gz
samtools faidx IRGSP-1.0_genome.fasta 
jbrowse add-assembly IRGSP-1.0_genome.fasta --load copy
gt gff3 -sortlines -tidy -retainids IRGSP-1.0_representative/locus.gff > IRGSP-1.0_representative/locus.sorted.gff
bgzip IRGSP-1.0_representative/locus.sorted.gff 
tabix IRGSP-1.0_representative/locus.sorted.gff.gz
jbrowse add-track IRGSP-1.0_representative/locus.sorted.gff.gz --out /jbrowse2 --load copy