#-*- coding:utf-8 -*-
from core.battle.move.geometry import Coordinate
from core.battle.move.shape import Shape
from core.battle.buff import Buff
from core.clock import Clock
from core.tools import Pool


class Object(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		self.shape = kwargs.get('shape')

		self.parent = kwargs.get('parent')

		self.children = []

		#跟随，技能移动时是否根据物体动态坐标实时计算位置，如钩子
		#self.follow = kwargs.get('follow', False)

		#碰撞时能否穿过
		self.across = kwargs.get('across', False)

		#碰撞后给碰撞的物体施加的buff
		self.collide_buffpool = Pool()

		self.buffpool = Pool()

		#self.buffpool.insert(BuffMove(source_object=self, route=None))

		self.life = 5.0
		self.attack = 2.0
		self.defense = 1.0


	def collide(self, obj):
		if self.shape.collide(obj.shape):
			self._collide(obj)
			obj._collide(self)
			return True
		return False

	def _collide(self, obj):
		self.buffpool.add(obj.collide_buffpool, source_object=self, target_object=obj)

	def select(self, operate):
		pass

	#获取附近的物体
	def get_beside(self):
		return [self]

	@classmethod
	def sample(self):
		return Object()

	@classmethod
	def test(self):
		obj1 = Object.sample()
		obj1.shape = Shape.sample()
		obj1.collide_buffpool.insert(Buff.sample())

		obj2 = Object.sample()
		obj2.shape = Shape.sample()
		obj2.collide_buffpool.insert(Buff.sample())

		obj1.collide(obj2)
		print obj1.buffpool.pool