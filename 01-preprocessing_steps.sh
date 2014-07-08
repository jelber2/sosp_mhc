#1)Copy zipped sff file to work directory
    cp /home/jelber2/Dropbox/sosp_mhc/454Sequences/TaylorSff03012011.zip /work/jelber2/sosp_mhc/rawdata/TaylorSff03012011.zip

#2)Unzip sff file in work directory
    unzip /work/jelber2/sosp_mhc/rawdata/TaylorSff03012011.zip 

#3)Rename unzipped sff file to TaylorSff03012011.sff
    mv GYQGN9104.sff TaylorSff03012011.sff

#4)Unzip TaylorB.zip from Justin Lock, but only extract the TaylorB.txt file (the mapping file) and copy it to the work directory
#the mapping file TaylorSff03012011-map.txt contains a tab-delimited file with column headings
#SampleID	BarcodeSequence	LinkerPrimerSequence	Description
    unzip -p /home/jelber2/Dropbox/sosp_mhc/454Sequences/TaylorB.zip \*.txt > /work/jelber2/sosp_mhc/rawdata/TaylorSff03012011-map.txt
#Qiime's ampliconnoise.py needs the -map.txt file

#5)Retain only lines not containing kiwa sequences (i.e., get rid of kiwa sequences) using awk
    awk '!/kiwa/' /work/jelber2/sosp_mhc/rawdata/TaylorSff03012011-map.txt > /work/jelber2/sosp_mhc/rawdata/TaylorSff03012011-map.nokiwa.txt

#6)Copy files using rsync from local machine to supermikeII (remove '--dry-run' at end of line to actually excute the command)
    rsync --archive --stats --progress /work/jelber2/sosp_mhc/ jelber2@mike.hpc.lsu.edu:/work/jelber2/sosp_mhc/ --dry-run
