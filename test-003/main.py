#-*- coding:utf-8 -*-
import os
import sys
path = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(path)
sys.path.append('.') #���ӵ�����·��

from core.test import autotest

if __name__ == '__main__':
	from core.clock import Clock
	autotest(allow=['core.battle.move.route'], ignore=['design', 'core'])
	Clock.sleep(1000)