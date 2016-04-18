#-*- coding:utf-8 -*-

class Buff(object):
	def __init__(self, **kwargs):
		pass


class BuffPool(object):
	def __init__(self, **kwargs):
		self.buffpool = []
	
	def insert(self, buff):
		self.buffpool.append(buff)
	
	def delete(self, buff):
		pass

	def __iadd__(self, other):
		self.buffpool += other.buffpool
