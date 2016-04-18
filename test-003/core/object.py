#-*- coding:utf-8 -*-
from core.battle.move.geometry import Coordinate
from core.battle.buff import Buff, BuffPool

class Object(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)
		
		self.parent = kwargs.get('parent')
		
		self.children = []
		
		#��ײ�����ײ������ʩ�ӵ�buff
		self.collide_change = BuffPool()
		
		self.buffpool = BuffPool()
	
	def select(self, operate):
		pass

	@classmethod
	def sample(self):
		return Object()