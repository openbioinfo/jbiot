#!/usr/bin/env python
from collections import OrderedDict
import os
import logging

def findDockerSingul(item):
    items = item.split()
    docker=""
    sing = ""
    for item in items:
        if item.startswith("--docker="):
            docker = item.split("=")[-1]
        if item.startswith("--singularity="):
            sing = item.split("=")[-1]
    docker=docker.strip()
    sing = sing.strip()
    return docker,sing

def handleSing(simg):
    sdir = "~/.singularity"
    if not os.path.exists(sdir):
        os.system("mkdir %s" % sdir)
    simgPath = os.path.join(sdir,simg)
    if os.path.exists(simgPath):
        return simg
    simghttp = "http://www.genescret.com:6636/singularity/%s" % simg
    cmd = "wget -P %s %s" % (sdir,simghttp)
    flag = os.system(cmd)
    if flag == 0:
        return simgPath
    msg = "%s not found" % simg
    logging.warning(msg)
    return 

def dockersing(cmdfile,prefer="docker"):
    fp = open(cmdfile)
    lines = fp.readlines()
    
    items = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        items.append(line)

    cmddict = OrderedDict()
    curkey = items[0]
    cmddict[curkey] = []
    for item in items[1:]:
        if item.startswith("#"):
            cmddict[item] = []
            curkey = item
        else:
            cmddict[curkey].append(item)

    afterDict = OrderedDict()
    for tag,cmds in cmddict.items():
        docker,sing = findDockerSingul(tag)
        if sing:
            sing = handleSing(sing)
        if not ( docker or sing ):
            afterDict[tag] = cmds
            continue
        
        vcmds = []
        for cmd in cmds:
            vcmd = cmd
            rootDir = "/rootDir"
            cmdelements = cmd.split()
            for i in range(len(cmdelements)):
                element = cmdelements[i]
                if element.startswith("/"):
                    element = rootDir + element
                    cmdelements[i] = element
            cmd = " ".join(cmdelements)
            dcmd = ""
            scmd = ""
            if docker :
                dcmd = "docker run --rm -v /:%s -v $PWD:$PWD -w $PWD %s %s" % (rootDir,docker,cmd)
            if sing:
                scmd = "singularity exec --bind /:%s %s %s " % (rootDir,sing,cmd)
            if  dcmd and scmd and prefer=="docker":
                vcmd = dcmd
            if dcmd and scmd and prefer=="singularity":
                vcmd = scmd
            if dcmd and not scmd:
                vcmd = dcmd
            if scmd and not dcmd:
                vcmd = scmd
       
            vcmds.append(vcmd)
        
        afterDict[tag] = vcmds


    afterFile = cmdfile.split(".")[0] + ".dockersing.cmd"
    fp = open(afterFile,"w")
    for tag,cmds in afterDict.items():
        line = "\n" + tag + "\n\n"
        fp.write(line)

        for cmd in cmds:
            line = "\t" + cmd + "\n"
            fp.write(line)
    fp.close()

    return afterFile

if __name__ == "__main__":
    from docopt import docopt

    usage = """
    Usage:
        dockersing.py <cmdfile> [--prefer=<docker|singularity>]

    Options:
        -h,--help           will print this screen
        <cmdfile>           cmdfile mostly generated by logrun or file with logrun style
        --prefer=<tech>     choose to prefer  [docker|singularity] when both exist [default: docker].

    """ 
    args = docopt(usage)
    cmdfile = args["<cmdfile>"]
    prefer = args["--prefer"] 
    if prefer not in ["docker","singularity"]:
        print usage
        sys.exit()
    dockersing(cmdfile,prefer) 