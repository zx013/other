#-*- coding:utf-8 -*-
from core.battle.move.geometry import Coordinate
from core.tools import Pool, Unit


class Object(Coordinate, Unit):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)
		Unit.__init__(self, **kwargs)

		self.parent = kwargs.get('parent')

		self.children = []

		#���棬�����ƶ�ʱ�Ƿ�������嶯̬����ʵʱ����λ�ã��繳��
		#self.follow = kwargs.get('follow', False)

		#��ײʱ�ܷ񴩹�
		self.across = kwargs.get('across', False)

		#��ײ�����ײ������ʩ�ӵ�buff
		self.collide_buffpool = Pool()

		self.buffpool = Pool()

		#self.buffpool.insert(BuffMove(source_object=self, route=None))

		self.life = 5.0
		self.attack = 2.0
		self.defense = 1.0

	def add(self, child):
		child.parent = self
		self.children.append(child)

	def collide(self, obj):
		if self.shape.collide(obj.shape):
			self._collide(obj)
			obj._collide(self)
			return True
		return False

	def _collide(self, obj):
		#��ΪObject����Skill��ȡ��parent
		source_object = self if type(self) is Object else self.parent
		target_object = obj if type(obj) is Object else obj.parent
		self.buffpool.add(obj.collide_buffpool, source_object=source_object, target_object=target_object)

	def select(self, operate):
		pass

	@classmethod
	def sample(self):
		return Object()

	@classmethod
	def test(self):
		from core.battle.move.shape import Shape
		from core.battle.buff import Buff
		
		obj1 = Object.sample()
		obj1.shape = Shape.sample()
		obj1.collide_buffpool.insert(Buff.sample())

		obj2 = Object.sample()
		obj2.shape = Shape.sample()
		obj2.collide_buffpool.insert(Buff.sample())

		print obj1.buffpool.pool, obj2.buffpool.pool
		obj1.collide(obj2)
		print obj1.buffpool.pool, obj2.buffpool.pool