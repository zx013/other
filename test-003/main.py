#-*- coding:utf-8 -*-
import os
import sys
path = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(path)
sys.path.append('.') #Ìí¼Óµ½ËÑË÷Â·¾¶

if __name__ == '__main__':
	from core.tools import Iterate
	Iterate.test()

	from core.battle.move.shape import Rect, Sector, Shape
	Rect.test()
	Sector.test()
	Shape.test()

	from core.battle.move.route import Line, Arc, Route
	Line.test()
	Arc.test()
	Route.test()

	from core.battle.skill import Skill
	Skill.test()