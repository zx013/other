#-*- coding:utf-8 -*-
from core.battle.move.geometry import Coordinate

class Object(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

	@classmethod
	def sample(self):
		return Object()