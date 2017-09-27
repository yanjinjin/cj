#coding=utf-8# -*- coding: UTF-8 -*-
import os
curdir = os.path.dirname(__file__)
import sys
sys.path.append(curdir)
import logging,time

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=os.path.join(curdir,'cj.log'),
                filemode='a')

def plog(mess):
    logging.info(mess)

