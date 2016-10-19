SOSP_MHC
========
###Last modified: 27 May 2015, 10:56h
========
#Get mothur
    cd ~/bin/
    mkdir mothur-1.35.0
    cd mothur-1.35.0
    wget https://github.com/mothur/mothur/releases/download/v1.35.0/Mothur.cen_64.zip
    unzip Mothur.cen_64.zip
    #PATH to mothur executable = /home/jelber2/bin/mothur-1.35.0/mothur/mothur
#Setup directories
    cd /work/jelber2/
    mkdir SOSP_MHC
    cd SOSP_MHC
    mkdir rawdata
    mkdir mothur_analyses
    cd mothur_analyses
#Get rawdata
    cd /work/jelber2/SOSP_MHC/rawdata
    # raw,zipped 454 sequences
    cp /work/jelber2/sosp_mhc/rawdata/TaylorSff03012011.zip .
    unzip TaylorSff03012011.zip
    mv GYQGN9104.sff TaylorSff03012011.sff
    # file with barcode sequences to demultiplex reads from sparrows
    cp /work/jelber2/sosp_mhc/rawdata/TaylorSff03012011.noprimers.oligos .
#Process files with mothur
##1.convert sff file (raw 454 data) into fasta and qual file with mothur's sffinfo
    /work/jelber2/SOSP_MHC/mothur_analyses
    mkdir sffinfo
    cd sffinfo
    # initiate mothur
    ~/bin/mothur-1.35.0/mothur/mothur
    # use sffinfo
    sffinfo(sff=/work/jelber2/SOSP_MHC/rawdata/TaylorSff03012011.sff, fasta=T, qfile=T, trim=T, flow=F, outputdir=/work/jelber2/SOSP_MHC/mothur_analyses/sffinfo/)
    # use summary.seqs
    summary.seqs(fasta=/work/jelber2/SOSP_MHC/mothur_analyses/sffinfo/TaylorSff03012011.fasta)
    quit()
    # Summary of TaylorSff03012011.fasta
    #		Start	End	NBases	Ambigs	Polymer	NumSeqs
    #Minimum:	1	39	39	0	1	1
    #2.5%-tile:	1	44	44	0	2	3943
    #25%-tile:	1	80	80	0	3	39423
    #Median: 	1	118	118	0	4	78846
    #75%-tile:	1	221	221	0	4	118268
    #97.5%-tile:	1	242	242	0	5	153748
    #Maximum:	1	980	980	43	16	157690
    #Mean:	1	140.122	140.122	0.0127402	3.64383
    # of Seqs:	157690
##2.Used mothur's trim.seqs to trim off low quality bases
    cd /work/jelber2/SOSP_MHC/mothur_analyses
    mkdir trim.seqs
    cd trim.seqs
    # initiate mothur
    ~/bin/mothur-1.35.0/mothur/mothur
    trim.seqs(fasta=/work/jelber2/SOSP_MHC/mothur_analyses/sffinfo/TaylorSff03012011.fasta, oligos=/work/jelber2/SOSP_MHC/rawdata/TaylorSff03012011.noprimers.oligos, minlength=140, maxlength=400, bdiffs=1, maxambig=2, maxhomop=10, qfile=/work/jelber2/SOSP_MHC/mothur_analyses/sffinfo/TaylorSff03012011.qual, qwindowsize=50, qwindowaverage=35, outputdir=/work/jelber2/SOSP_MHC/mothur_analyses/trim.seqs/, processors=2)
    summary.seqs(fasta=/work/jelber2/SOSP_MHC/mothur_analyses/trim.seqs/TaylorSff03012011.trim.fasta)
    quit()
    # Summary of TaylorSff03012011.trim.fasta
    #		Start	End	NBases	Ambigs	Polymer	NumSeqs
    #Minimum:	1	140	140	0	1	1
    #2.5%-tile:	1	142	142	0	4	173
    #25%-tile:	1	209	209	0	4	1729
    #Median: 	1	226	226	0	4	3458
    #75%-tile:	1	227	227	0	5	5186
    #97.5%-tile:	1	230	230	0	5	6742
    #Maximum:	1	334	334	1	6	6914
    #Mean:	1	209.918	209.918	0.00144634	4.25644
    # of Seqs:	6914
##3.Used mothur's chimer.uchime to remove chimera sequences.
    cd /work/jelber2/SOSP_MHC/mothur_analyses/
    mkdir chimera.uchime
    cd chimera.uchime
    # initiate mothur
    ~/bin/mothur-1.35.0/mothur/mothur
    # use uchime to get rid of chimeras
    chimera.uchime(fasta=/work/jelber2/SOSP_MHC/mothur_analyses/trim.seqs/TaylorSff03012011.trim.fasta, reference=self, processors=2, dereplicate=f, chimealns=t, abskew=1.9, minh=0.3, mindiv=0.5, xn=8.0, dn=1.4, xa=1, chunks=4, minchunk=64, idsmoothwindow=32, maxp=2, skipgaps=t, skipgaps2=t, minlen=140, maxlen=400, ucl=f, outputdir=/work/jelber2/SOSP_MHC/mothur_analyses/chimera.uchime/)
    remove.seqs(accnos=/work/jelber2/SOSP_MHC/mothur_analyses/chimera.uchime/TaylorSff03012011.trim.uchime.accnos, fasta=/work/jelber2/SOSP_MHC/mothur_analyses/trim.seqs/TaylorSff03012011.trim.fasta, group=/work/jelber2/SOSP_MHC/mothur_analyses/trim.seqs/TaylorSff03012011.groups, qfile=/work/jelber2/SOSP_MHC/mothur_analyses/trim.seqs/TaylorSff03012011.trim.qual, outputdir=/work/jelber2/SOSP_MHC/mothur_analyses/chimera.uchime/)
    quit()
    mv TaylorSff03012011.trim.pick.fasta TaylorSff03012011.trim.nochimera.fasta
    mv TaylorSff03012011.trim.pick.qual TaylorSff03012011.trim.nochimera.qual
    mv TaylorSff03012011.pick.groups TaylorSff03012011.trim.nochimera.groups
    ~/bin/mothur-1.35.0/mothur/mothur
    summary.seqs(fasta=/work/jelber2/SOSP_MHC/mothur_analyses/chimera.uchime/TaylorSff03012011.trim.nochimera.fasta)
    quit()
    # Summary of TaylorSff03012011.trim.seqtrim.nochimera.fasta
    #		Start	End	NBases	Ambigs	Polymer	NumSeqs
    #Minimum:	1	140	140	0	1	1
    #2.5%-tile:	1	142	142	0	4	171
    #25%-tile:	1	209	209	0	4	1702
    #Median: 	1	226	226	0	4	3404
    #75%-tile:	1	227	227	0	5	5105
    #97.5%-tile:	1	230	230	0	5	6636
    #Maximum:	1	334	334	1	6	6806
    #Mean:	1	209.825	209.825	0.00146929	4.25595
    # of Seqs:	6806
##4.Used mothur's rename.seqs and awk to add sample ids to fasta headers
    cd /work/jelber2/SOSP_MHC/mothur_analyses/chimera.uchime/
    # change fasta headers from >GYQGN9104J14BW bdiffs=0(match) fpdiffs=0(match)         xy=4007_2522
    #                        to >GYQGN9104J14BW
    perl -pe "s/(>\w+)\t.+\n/\1\n/" TaylorSff03012011.trim.nochimera.fasta > TaylorSff03012011.trim.nochimera.temp.fasta
    # initiate mothur
    ~/bin/mothur-1.35.0/mothur/mothur
    # use rename.seqs to add sparrow ids to fasta header
    rename.seqs(fasta=/work/jelber2/SOSP_MHC/mothur_analyses/chimera.uchime/TaylorSff03012011.trim.nochimera.temp.fasta, group=/work/jelber2/SOSP_MHC/mothur_analyses/chimera.uchime/TaylorSff03012011.trim.nochimera.groups)
    quit()
    # rename TaylorSff03012011.trim.nochimera.temp.renamed.fasta to TaylorSff03012011.trim.nochimera.renamed.fasta
    mv TaylorSff03012011.trim.nochimera.temp.renamed.fasta TaylorSff03012011.trim.nochimera.renamed.fasta
##5.Trim forward and reverse primers
    # forward primer = GAAAGCTCGAGTGTCACTTCACGAACGGC (5'to3')
    # reverse primer = GGGTGACAATCCGGTAGTTGTGCCGGCAG (5'to3')
    #
    # trim the forward primer using the last 8bp in 5'to3' orientation
    # looks for up to 50 bases followed by primer
    perl -pe "s/(^\\w{0,50}CGAACGGC)//g" TaylorSff03012011.trim.nochimera.renamed.fasta > test
    # trim the reverse primer using the last 8bp in 5'to3' orientation
    # looks for up to 50 bases followed by primer
    perl -pe "s/(^\\w{0,50}GCCGGCAG)//g" test > test2
    # trim the forward primer using the last 8bp of forward primer in 3' to 5' orientation (reverse complement)
    # looks for reverse complement of forward primer up to 50 bases from end of sequence
    perl -pe "s/(GCCGTTCG\w{0,60}$)//g" test2 > test3
    # trim the reverse primer using the last 8bp of reverse primer in 3' to 5' orientation (reverse complement)
    # looks for reverse complement of reverse primer up to 50 bases from end of sequence
    perl -pe "s/(CTGCCGGC\w{0,60}$)//g" test3 > test4
    mv test4 TaylorSff03012011.trim.nochimera.renamed.noprimers.fasta
    # make new directory for upcoming new file *.sequencher.fasta
    cd /work/jelber2/SOSP_MHC/mothur_analyses/
    mkdir align.seqs
    cd align.seqs
    # use Sequencher to trim off the remaining forward and reverse primers
    # by setting the primers as reference sequences, then aligning to the
    # the forward primer, next trimming off the forward primer from the reads,
    # finally repeating those steps with the reverse primers
    # saved file as TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.fasta
##6.Use Align.seqs to align seqs to a template/reference
    #
    # note: used Genbank accession: JX214349.1 as template!
    # Geothlypis trichas MHC class II beta antigen (Getr-DAB) gene, Getr-DAB*250 allele, exon 2 and partial cds
    # get in the correct working directory
    cd /work/jelber2/SOSP_MHC/mothur_analyses/align.seqs
    #
    # initiate mothur
    ~/bin/mothur-1.35.0/mothur/mothur
    # use align.seqs, use flip=t to try reverse complement
    align.seqs(candidate=TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.fasta, template=JX214349.1.fasta, flip=t, processors=2)
    summary.seqs(fasta=TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.align)
    quit()
    # Summary of TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.align
    #		Start	End	NBases	Ambigs	Polymer	NumSeqs
    #Minimum:	1	1	1	0	1	1
    #2.5%-tile:	42	158	11	0	2	171
    #25%-tile:	48	176	129	0	4	1702
    #Median: 	48	220	173	0	4	3404
    #75%-tile:	48	220	173	0	5	5105
    #97.5%-tile:	254	270	174	0	5	6636
    #Maximum:	270	270	201	1	6	6806
    #Mean:	55.2731	203.874	149.55	0.000881575	4.18366
    # of Seqs:	6806
    # Note: nearly all of the sequences 5105 (75%-tile) out of 6806 align/occur
    # within bases 48-220 of the template
##7.Screen.seqs to get only bases b/w 48-220
    # initiate mothur
    ~/bin/mothur-1.35.0/mothur/mothur
    # screen.seqs, start and end are what you think they mean
    screen.seqs(fasta=TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.align, start=48, end=220, group=/work/jelber2/SOSP_MHC/mothur_analyses/chimera.uchime/TaylorSff03012011.trim.nochimera.renamed.groups)
    summary.seqs(fasta=TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.align)
    quit()
    # Summary of TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.align
    #		Start	End	NBases	Ambigs	Polymer	NumSeqs
    #Minimum:	20	220	170	0	3	1
    #2.5%-tile:	47	220	172	0	4	106
    #25%-tile:	48	220	173	0	4	1055
    #Median: 	48	220	173	0	4	2109
    #75%-tile:	48	220	173	0	5	3163
    #97.5%-tile:	48	221	176	0	5	4111
    #Maximum:	48	247	201	1	6	4216
    #Mean:	47.8287	220.128	173.249	0.000711575	4.30028
    # of Seqs:	4216
##8.Filter.seqs to get rid of gaps (.) in alignment
    # initiate mothur
    ~/bin/mothur-1.35.0/mothur/mothur
    # filter.seqs, trump=. means get rid of gaps designated by "."
    filter.seqs(fasta=TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.align, trump=., vertical=F)
    summary.seqs(fasta=TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.filter.fasta)
    quit()
    # Summary of TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.filter.fasta
    #		Start	End	NBases	Ambigs	Polymer	NumSeqs
    #Minimum:	1	173	169	0	3	1
    #2.5%-tile:	1	173	172	0	4	106
    #25%-tile:	1	173	173	0	4	1055
    #Median: 	1	173	173	0	4	2109
    #75%-tile:	1	173	173	0	5	3163
    #97.5%-tile:	1	173	173	0	5	4111
    #Maximum:	2	173	173	1	6	4216
    #Mean:	1.00024	173	172.951	0.000711575	4.29981
    # of Seqs:	4216
##9.Subsample (rarefaction, keeping 10 sequences per individual) because control sample over-represented
    # initiate mothur
    ~/bin/mothur-1.35.0/mothur/mothur
    sub.sample(fasta=TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.filter.fasta, group=TaylorSff03012011.trim.nochimera.renamed.good.groups, persample=true, size=10)
    # from 4216 to 160 reads (many individuals had < 10 sequences)
    # Output File Names: 
    # TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.filter.subsample.fasta
    summary.seqs(fasta=TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.filter.subsample.fasta)
    quit()
    # Summary of TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.filter.subsample.fasta
    #		Start	End	NBases	Ambigs	Polymer	NumSeqs
    #Minimum:	1	173	172	0	4	1
    #2.5%-tile:	1	173	172	0	4	5
    #25%-tile:	1	173	173	0	4	41
    #Median: 	1	173	173	0	4	81
    #75%-tile:	1	173	173	0	5	121
    #97.5%-tile:	1	173	173	0	5	157
    #Maximum:	1	173	173	0	5	160
    #Mean:	1	173	172.963	0	4.48125
    # of Seqs:	160
##10.Get alleles
    # a.Use PGDSpider 2.8.03 to convert
    #   TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.filter.subsample.fasta to genepop format
    # b.Saved as TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.filter.subsample.alleles.txt
    # NOTE: ALSO copied the log output which contains information such as:
    #   INFO  01:01:01 - Allele "AGCATANATA" converted to "1"\r\n
    #   INFO  01:01:01 - Allele "AGCATACATA" converted to "2"\r\n
    #   Copied allele information into NOTEPAD ++ then used the following regular expressions to convert to allele\tsequence
    #   find: INFO  \d+:\d+:\d+ - Allele "(\w+)" converted to "(\d+)"\r\n
    #   replace: \2\t\1
    # c.Use regular expressions to rename the sample_ids from GYQGN9104H58GD_SROS2 to SROS2
        i.find \w+_(\w+) ,  (\d+\r\n)
        ii.replace \1\t\2
        iii.rename file as TaylorSff03012011.trim.nochimera.renamed.noprimers.sequencher.good.filter.subsample.alleles.renamed.txt
    # d.Open in Excel and sort by sample_id then by allele#
