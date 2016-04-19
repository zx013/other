#-*- coding:utf-8 -*-
import os
import sys
path = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(path)
sys.path.append('.') #Ìí¼Óµ½ËÑË÷Â·¾¶

from core.test import autotest

if __name__ == '__main__':
	from core.clock import Clock
	autotest(allow=[], ignore=['design', 'core.battle.move'])
	Clock.sleep(100)