#!/usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from wxpy import *
from wechat_sender import *
import os
from sysinfo import meminfo,cpuinfo,diskinfo 

home = os.environ["HOME"]
whome = os.path.join(home,".wexin")
botpk = os.path.join(whome,"bot.pk1")

if not  os.path.exists(whome):
    cmd = "mkdir -p %s" % whome
    os.system(cmd)

bot = Bot(botpk,console_qr=False)

groups = bot.groups()
grp = groups.search(u"生信研发群")[0]

friends = bot.friends()
deju = friends.search("D J. Kong")[0]
tuling = Tuling(api_key='184299f0a24146128073f5bc60e91812')

def jbioreply(msg):
    msgstr = msg.text
    print msgstr
    if msgstr.find(u"@晶宝") != -1:
        tuling.do_reply(msg)
    if msgstr == "sysinfo":
        disk = diskinfo()
        msg.reply(disk)
        mem = meminfo()
        msg.reply(mem)
        cpu = cpuinfo()
        msg.reply(cpu)

@bot.register(deju)
def reply_deju(msg):
    jbioreply(msg)

@bot.register(grp)
def reply_devlab(msg):
    jbioreply(msg) 

#listen(bot,token="devlab",receivers=[deju])

