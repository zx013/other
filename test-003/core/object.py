#-*- coding:utf-8 -*-
from core.battle.move.geometry import Coordinate
from core.battle.move.shape import Shape
from core.battle.move.route import Route
from core.battle.buff import Buff, BuffPool
from core.clock import Clock
from core.event import trigger, untrigger


#每个时间片计算地图中所有碰撞的物体对（计算所有包含移动Buff的物体）
#每个物体移动时的碰撞直接获取结果（物体碰撞到的其它物体）
class BuffMove(Buff):
	'''
		沿着轨迹移动
	'''
	def __init__(self, object, **kwargs):
		Buff.__init__(self, **kwargs)

		self.event = ('TIME_EVENT', 'TIMER')

		#buff所在的object或skill
		self.object = object

	#添加路径
	def add_route(self, route):
		self.del_route()
		self.object.route = route
		#self.adjust_to_map()
		trigger(self.event, self.run)

	#移除路径
	def del_route(self):
		untrigger(self.event, self.run)

	def turn(self, rotate1, rotate2):
		#print rotate1, rotate2
		self.object.set_rotate(rotate2)

	def move(self, offset1, offset2):
		#print offset1, offset2
		self.object.set_offset(offset2)

	def collide(self, frame):
		for f in frame:
			pass
		return []

	#一个时间片的移动（旋转）
	def run(self):
		for step in self.object.route.move():
			print step
			if step['type'] == 'rotate':
				self.turn(step['start'], step['end'])
			elif step['type'] == 'move':
				collide = self.collide(step['frame'])
				for obj in collide:
					obj.buffpool += self.object.collide_change
					self.object.buffpool += obj.collide_change
				if self.object.across or not collide:
					self.move(step['start'], step['end'])
			yield

	@classmethod
	def sample(self):
		return BuffMove(Object.sample())

	@classmethod
	def test(self):
		buffmove = BuffMove.sample()
		buffmove.add_route(Route.sample())
		#buffmove.delete()


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

		self.buffpool.insert(BuffMove(self))

	def add(self, shape):
		self.shape = kwargs['shape']

	def select(self, operate):
		pass

	@classmethod
	def sample(self):
		return Object()