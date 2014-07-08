#! /usr/bin/env python

# PBS cluster job submission in Python
# Uses Ampliconnoise to denoise, demultiplex,
# remove chimeras from 454 flowgram files
# By Jean P. Elbers
# jelber2@lsu.edu
# Last modified 8 July 2014
###############################################################################
Usage = """

03-denoise.py - version 1.0
STEPS:
1.Use mothur's implementation of ampliconnoise
    /usr/local/packages/bioinformatics/qiime/1.7.0/python/bin/ampliconnoise.py \
    -i Sample.sff.txt \
    -m Sample-map.nokiwa.txt \
    -o ../denoised/Sample-nokiwa-ampliconnoise.fna \
    -n 4 \
    -f \
    --platform titanium

Directory info:
InDir = /work/jelber2/sosp_mhc/rawdata/
OutDir = /work/jelber2/sosp_mhc/denoised/
Output Files = Sample-ampliconnoise.fna

Usage (execute following code in InDir):

~/scripts/sosp_mhc/03-denoise.py Sample.sff.txt

"""
###############################################################################
import os, sys, subprocess, re #imports os, sys, subprocess, re modules


if len(sys.argv)<2:
    print Usage
else:
    FileList = sys.argv[1:]
    InDir = "/work/jelber2/sosp_mhc/rawdata/"
    OutDir = "/work/jelber2/sosp_mhc/denoised/"
    os.chdir(InDir)
    for InFileName in FileList:
        FileSuffix = ".sff.txt" # string to remove from InFileName
        Sample = InFileName.replace(FileSuffix,'') # creates Sample string
        # Customize your options here
        Queue = "single"
        Allocation = "hpc_startup_jelber2"
        Processors = "nodes=1:ppn=4"
        WallTime = "72:00:00"
        LogOut = OutDir
        LogMerge = "oe"
        JobName = "denoise-%s" % (Sample)
        Command ="""
        /usr/local/packages/bioinformatics/qiime/1.7.0/python/bin/ampliconnoise.py \
        -i %s.sff.txt \
        -m %s-map.nokiwa.txt \
        -o ../denoised/%s-nokiwa-ampliconnoise.fna \
        -n 4 \
        -f \
        --platform titanium""" % (Sample, Sample, Sample)

        JobString = """
        #!/bin/bash
        #PBS -q %s
        #PBS -A %s
        #PBS -l %s
        #PBS -l walltime=%s
        #PBS -o %s
        #PBS -j %s
        #PBS -N %s

        cd %s
        %s\n""" % (Queue, Allocation, Processors, WallTime, LogOut, LogMerge, JobName, InDir, Command)

        #Create pipe to qsub
        proc = subprocess.Popen(['qsub'], shell=True,
          stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        (child_stdout, child_stdin) = (proc.stdout, proc.stdin)

        #Print JobString
        jobname = proc.communicate(JobString)[0]
        print JobString
        print jobname
