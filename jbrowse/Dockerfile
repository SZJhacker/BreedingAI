FROM node
ADD sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y genometools samtools tabix 
WORKDIR /jbrowse2
RUN npm install -g @jbrowse/cli
RUN jbrowse create jbrowse2


# COPY ./docker-entrypoint.sh /jbrowse2/docker-entrypoint.sh
COPY ./IRGSP-1.0_genome.fasta.gz ./IRGSP-1.0_representative_2021-05-10.tar.gz ./install.sh /jbrowse2/
RUN /bin/bash install.sh
# COPY ./IRGSP-1.0_representative_2021-05-10.tar.gz /jbrowse2/

# RUN gzip -d /jbrowse2/IRGSP-1.0_genome.fasta.gz && tar -zxvf /jbrowse2/IRGSP-1.0_representative_2021-05-10.tar.gz
# # RUN tar -zxvf /jbrowse2/IRGSP-1.0_representative_2021-05-10.tar.gz

# RUN samtools faidx IRGSP-1.0_genome.fasta && jbrowse add-assembly IRGSP-1.0_genome.fasta --load copy
# RUN gt gff3 -sortlines -tidy -retainids IRGSP-1.0_representative/locus.gff > IRGSP-1.0_representative/locus.sorted.gff
# RUN bgzip IRGSP-1.0_representative/locus.sorted.gff 
# RUN tabix IRGSP-1.0_representative/locus.sorted.gff.gz
# RUN jbrowse add-track IRGSP-1.0_representative/locus.sorted.gff.gz --out /jbrowse2 --load copy
VOLUME [ "/jbrowse2" ]

RUN npm install http-server -g
CMD ["npx","http-server", "-a","0.0.0.0","-p", "5001"]

