#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import gzip, re
import pandas as pd
import numpy as np

class GenomeFeature:
    GEN_BIN = {
        "./.": 0, ".|.": 0, "0/0": 0, "0|0": 0, "0/1": 1, "0|1": 1, "1/0": 1,
        "1|0": 1, "1/1": 2, "1|1": 2
    }

    def __init__(self, gff_file, vcf_file, outfile):
        self.gff_file = gff_file
        self.vcf_file = vcf_file
        self.outfile = outfile
        self.meta_info = []
        self.header_info = []
        self.descriptor = {}

    def site_location(self, site, start, end):
        """determine whether the SNP site is in a certain region"""
        return start <= site <= end

    def gentoye2genobin(self, genotypes):
        """convert SNPs into genotypes"""
        return [self.GEN_BIN.get(genotype, 0) for genotype in genotypes]

    def vcf_info_parse(self, line):
        """parse information from vcf line"""
        vcf_info_list = line.strip().split('\t')
        chrom = vcf_info_list[0]
        position = vcf_info_list[1]
        sample_genotype = self.gentoye2genobin(
            [varients.split(':')[0] for varients in vcf_info_list[9:]])
        return chrom, position, np.array(sample_genotype, dtype=np.int8)

    def gff_info_parse(self, line):
        """parse information from gff line"""
        chrom, _, _, start, end, _, _, _, info = line
        geneid_pre = re.search('ID=([0-9A-Za-z:]+);', info).group(1)
        geneid = re.sub('gene:', '', geneid_pre, re.I)
        return chrom, start, end, geneid

    def parse(self):
        anchor = False
        with gzip.open(self.gff_file, mode='rt') as gffs, gzip.open(self.vcf_file, mode='rt') as vcf:
            for gff_records in gffs:
                gff_record = gff_records.strip().split('\t')
                biotype = gff_record[2:3]  # obtain the value with index 2, no error is reported when out of bounds (comment lines may not have 9 elements)
                if biotype and biotype[0] == 'gene':
                    chrom_gff, star, end, geneid = self.gff_info_parse(gff_record)
                    self.descriptor[geneid] = np.array([0])
                    if anchor and self.site_location(position, star, end):
                        self.descriptor[geneid] = self.descriptor[geneid] + genotypes
                        anchor = False
                    for line in vcf:
                        if not line.startswith("#"):
                            chrom_vcf, position, genotypes = self.vcf_info_parse(line)
                            if chrom_vcf == chrom_gff:
                                if position < star:
                                    continue
                                elif self.site_location(position, star, end):
                                    self.descriptor[geneid] = self.descriptor[geneid] + genotypes  #利用array的广播机制记录vcf的杂合性
                                else:
                                    anchor = True
                                    break
                            else:
                                anchor = True  # 染色体不一致的时候，vcf迭代到下一条染色体，跳出vcf文件的循环后应该进行一次vcf和gff文件的操作
                                break
                        elif line.startswith("##"):
                            self.meta_info.append(line.strip())
                        else:
                            self.header_info.append(line.strip())
        pd.DataFrame(self.descriptor,
                index=self.header_info[0].split('\t')[9:]).to_csv(self.outfile)