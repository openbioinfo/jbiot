import sys
import os
import subprocess

def status_run(cmdfile,wdir):
    cid = cmdfile.split("/")[-1].split(".")[0]
    cmdstatus = ".status"
    cmd = "mkdir -p %s" % cmdstatus
    os.system(cmd)
    logdir = ".log"
    cmd = "mkdir -p %s" % logdir
    os.system(cmd)
    logfile = os.path.join(logdir,cid+".log")

    cmd = "sh %s " % cmdfile
    fp = open(logfile,"w")
    statusfile = os.path.join(cmdstatus,cid+".status") 
    os.system("rm -f %s 1>>/dev/null 2>>/dev/null" % statusfile)
    p = subprocess.Popen(cmd,shell=True,stdout=fp,stderr=fp)
    code = p.wait()
    if not code:
        os.system("touch %s" % (statusfile))

    if wdir:
        statdir = os.path.join(wdir,".status/")
        cmd = "oss2tools.py upload %s %s" % (statusfile,statdir) 
        os.system(cmd)
        logdir = os.path.join(wdir,".log/")
        cmd = "oss2tools.py upload %s %s" % (logfile,logdir) 
        os.system(cmd)
