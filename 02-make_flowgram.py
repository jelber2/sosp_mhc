#! /usr/bin/env python

# PBS cluster job submission in Python
# Create flowgram for sosp_mhc reads
# By Jean P. Elbers
# jelber2@lsu.edu
# Last modified 8 July 2014
###############################################################################
Usage = """

02-make_flowgram.py - version 1.1
STEPS:
1.Use mothur's implementation of sffinfo to 
  convert sff file (raw 454 data) into sff.txt (flowgram format)
  Note that trimming is turned off by trim=f option
    /usr/local/packages/bioinformatics/qiime/1.7.0/bin/mothur "#sffinfo(sff=/work/jelber2/sosp_mhc/rawdata/Sample.sff, trim=f, sfftxt=T)"

Directory info:
InDir = /work/jelber2/sosp_mhc/rawdata/
OutDir = InDir
Output Files = Sample.sff.txt

Usage (execute following code in InDir):

~/scripts/sosp_mhc/02-make_flowgram.py Sample.sff

"""
###############################################################################
import os, sys, subprocess, re #imports os, sys, subprocess, re modules


if len(sys.argv)<2:
    print Usage
else:
    FileList = sys.argv[1:]
    InDir = "/work/jelber2/sosp_mhc/rawdata/"
    OutDir = InDir
    os.chdir(InDir)
    for InFileName in FileList: # 
        FileSuffix = ".sff" # string to remove from InFileName
        Sample = InFileName.replace(FileSuffix,'') # creates Sample string
        # Customize your options here
        Queue = "single"
        Allocation = "hpc_startup_jelber2"
        Processors = "nodes=1:ppn=1"
        WallTime = "24:00:00"
        LogOut = OutDir
        LogMerge = "oe"
        JobName = "make-flowgram-%s" % (Sample)
        Command ='''
        /usr/local/packages/bioinformatics/qiime/1.7.0/bin/mothur "#sffinfo(sff=/work/jelber2/sosp_mhc/rawdata/%s.sff, trim=f, sfftxt=T)"''' % (Sample)

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
