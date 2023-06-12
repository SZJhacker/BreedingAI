import os
import string

class Snake:
    template = string.Template("""
rule all:
    input:
        expand("${results_directory}/Out_{sample}_related_pairwise_pi.txt")

rule index:
    input:
        "${file_directory}/${sample}"
    output:
        "${file_directory}/${sample}.tbi"
    shell:
        "tabix -p vcf {input} "

rule homoanalysis:
    input:
        "${file_directory}/${sample}",
        "${file_directory}/${sample}.tbi"
    output:
        "${results_directory}/Out_{sample}_related_pairwise_pi.txt"
    log:
        "${sample}.log"
    script:
        "1_integrated_rice_homogeneity_analysis_pipeline.py -i {input[0]} -ii ${sample_id} -t 5 -l ${target} 1>{log} 2>&1 "

rule send:
    input:
        directory("${results_directory}")
    shell:
        "mutt -s '${topic}' ${email} -a {input}"
    """)

    def __init__(self):
        self.snake = ''

    def build(self, **kwargs):
        self.snake = self.template.substitute(kwargs)

    def save_file(self, name):
        with open(name, 'w') as f:
            f.write(self.snake)

    def run(self, name='Snakefile'):
        if os.path.exists(name):
            assert not os.system("snakemake -s {name}".format(name))
        else:
            self.save_file(name)
            self.run(name)
