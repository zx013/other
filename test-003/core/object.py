#-*- coding:utf-8 -*-
from core.battle.move.geometry import Coordinate
from core.battle.move.shape import Shape
from core.battle.move.route import Route
from core.battle.buff import Buff, BuffPool
from core.clock import Clock


class BuffAttack(Buff):
	def __init__(self, **kwargs):
		Buff.__init__(self, **kwargs)

		self.event = (('TIME_EVENT', 'TIMER'))

		self.object = kwargs['object']
	
	def run(self):
		pass
		#self.object.life



#每个时间片计算地图中所有碰撞的物体对（计算所有包含移动Buff的物体）
#每个物体移动时的碰撞直接获取结果（物体碰撞到的其它物体）
class BuffMove(Buff):
	#改变rotate, offset
	def __init__(self, **kwargs):
		Buff.__init__(self, **kwargs)

		self.event = ('MAP_EVENT', 'COLLIDE')

		#buff所在的object或skill
		self.object = kwargs['object']

		self.route = kwargs['route']

	def turn(self, rotate1, rotate2):
		#print rotate1, rotate2
		self.object.set_rotate(rotate2)

	def move(self, offset1, offset2):
		#print offset1, offset2
		self.object.set_offset(offset2)

	def back(self, offset1, offset2):
		self.object.set_offset(offset1)

	def collide(self, frame):
		return []

	#{'start': (1.5, 9.184850993605148e-17), 'frame': [(2.0, 1.2246467991473532e-16)], 'end': (2.0, 1.2246467991473532e-16), 'type': 'move'}
	#{'start': 90.0, 'end': 70.0, 'type': 'rotate'}
	#一个时间片的移动（旋转）
	def run(self):
		for step in self.route.move():
			print step
			if step['type'] == 'rotate':
				self.turn(step['start'], step['end'])
			elif step['type'] == 'move':
				self.move(step['start'], step['end'])
				collide = self.collide(step['frame'])
				for obj in collide:
					obj.buffpool += self.object.collide_change
					self.object.buffpool += obj.collide_change
				if not self.object.across and collide:
					raise
					self.back(step['start'], step['end'])
			yield

	@classmethod
	def sample(self):
		return BuffMove(object=Object.sample(), route=Route.sample())

	@classmethod
	def test(self):
		buffmove = BuffMove.sample()
		buffmove.create()
		#buffmove.destroy()


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
		self.collide_change = BuffPool()

		self.buffpool = BuffPool()

		self.buffpool.insert(BuffMove(object=self, route=None))

	def add(self, shape):
		self.shape = kwargs['shape']

	def select(self, operate):
		pass

	#获取附近的物体
	def get_beside(self):
		return [self]

	@classmethod
	def sample(self):
		return Object()