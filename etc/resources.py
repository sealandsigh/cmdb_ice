# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/21

import os

if __name__ =='__main__':
    fhandler = os.popen('top -n 1')
    flines = fhandler.readlines()
    cpuline = flines[2].split()
    memline = flines[3].split()
    cpu = float(cpuline[1])
    memtotal = float(memline[3])
    memuse = float(memline[7])
    mem = round(memuse / memtotal * 100,1)
    print(cpu,mem)