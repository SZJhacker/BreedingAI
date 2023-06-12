apt-get update && apt-get install -y vcftools tabix bcftools plink 
apt-get install -y dirmngr apt-transport-https ca-certificates software-properties-common gnupg2
apt-key adv --keyserver  keyserver.ubuntu.com  --recv-key E19F5F87128899B192B1A2C2AD5F960A256A04AF
apt-key adv --keyserver  keyserver.ubuntu.com  --recv-key FCAE2A0E115C3D8A
# add-apt-repository 'deb http://cloud.r-project.org/bin/linux/debian buster-cran40/'
apt-get update && apt-get install -y r-base
Rscript install.R