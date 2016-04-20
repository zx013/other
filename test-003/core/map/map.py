#-*- coding:utf-8 -*-


class Map(object):
	def __init__(self, **kwargs):
		self.objectpool = []
	
	def collide(self):
		collidepool = {}
		for obj1 in self.objectpool:
			for obj2 in self.objectpool:
				key = set((obj1, obj2))
				if collidepool.has_key(key):
					continue
				collidepool[key] = obj1.shape.collide(obj2.shape)