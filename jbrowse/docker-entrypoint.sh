#!/bin/bash
# for i in $(ls IRGSP-1.0_representative/*gff)
# do 
#     gt gff3 -sortlines -tidy -retainids $i > ${i/gff/sorted.gff} 1>test.log 2>&1 
#     bgzip ${i/gff/sorted.gff} 
#     tabix ${i/gff/sorted.gff}.gz
#     jbrowse add-track ${i/gff/sorted.gff} --out /jbrowse2 --load copy 
# done
npx serve -l 0.0.0.0:5001 /jbrowse2