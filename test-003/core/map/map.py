#-*- coding:utf-8 -*-
from core.event import signal, bind


class Map(object):
	def __init__(self, **kwargs):
		self.objectpool = []
		bind(('TIME_EVENT', 'TIMER'), self.collide)
	
	def collide(self):
		collidepool = {}
		for obj1 in self.objectpool:
			collidepool[obj1] = set()
			for obj2 in self.objectpool:
				if obj1.shape.collide(obj2.shape):
					collidepool[obj1].add(obj2)
		signal(('MAP_EVENT', 'COLLIDE'))

	@classmethod
	def sample(self):
		return Map()

	@classmethod
	def test(self):
		m = self.sample()