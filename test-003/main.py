#-*- coding:utf-8 -*-
import os
import sys
path = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(path)
sys.path.append('.') #���ӵ�����·��

from core.test import autotest

if __name__ == '__main__':
	autotest(ignore=['design', 'core.battle.move'])
	