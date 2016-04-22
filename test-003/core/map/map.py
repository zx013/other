#-*- coding:utf-8 -*-
from core.event import signal, bind


class Map(object):
	def __init__(self, **kwargs):
		self.objectpool = []
		bind(('TIME_EVENT', 'TIMER'), self.collide)
	
	#Åö×²£¬²¢½»»»×´Ì¬
	def collide(self):
		collidepool = set()
		for obj1 in self.objectpool:
			for obj2 in self.objectpool:
				if obj1.shape.collide(obj2.shape):
					obj1.buffpool += obj2.collide_change
					obj2.buffpool += obj1.collide_change
					collidepool.add(obj1)
					collidepool.add(obj2)
		signal(('MAP_EVENT', 'COLLIDE'))

	@classmethod
	def sample(self):
		return Map()

	@classmethod
	def test(self):
		m = Map.sample()