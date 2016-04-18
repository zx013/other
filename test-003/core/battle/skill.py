#-*- coding:utf-8 -*-
from core.battle.move.shape import Shape
from core.battle.move.route import Route
from core.battle.buff import Buff, BuffPool
from core.object import Object
from core.clock import Clock
from core.event import bind


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

		self.map_adjust()
		self.generator = self.object.route.move()

	def pre_move(self):
		pass

	def move(self):
		#先旋转，再移动
		#旋转的时间不到一个时间片则累计，直到有一个时间片长度时进行计时
		self.object.set_offset()
		#在轨迹上移动时朝向会随时变化
		self.object.set_rotate()

	def collide(self):
		return []

	#计算下一个点
	#移动到下一个点
	#计算碰撞
	def run(self):
		collide = self.collide()
		for obj in collide:
			obj.buffpool += self.obj.collide_change
			self.obj.buffpool += obj.collide_change
		if self.obj.across or not collide:
			self.move()

	#将坐标调整到地图坐标
	def map_adjust(self):
		self.object.shape.set_offset(self.object.parent.offset)
		self.object.shape.set_rotate(self.object.parent.rotate)
		self.object.route.set_offset(self.object.parent.offset)
		self.object.route.set_rotate(self.object.parent.rotate)


class Skill(Object):
	def __init__(self, **kwargs):
		Object.__init__(self, **kwargs)

		self.shape = kwargs['shape']

		self.route = kwargs['route']

		#跟随，技能移动时是否根据物体动态坐标实时计算位置，如钩子
		#self.follow = kwargs.get('follow', False)
		
		#碰撞时能否穿过
		self.across = kwargs.get('across', False)

		self.buffpool.insert(BuffMove(self))

	#默认传入的参数，source_object
	#选中一个目标，target_object
	#选中一个点，target_point
	#无
	def release(self, target=None):
		'''
		self.object release skill
			target is object, point or None
		'''
		if isinstance(target, Object):
			self._release_object(target)
		elif isinstance(target, tuple) or isinstance(target, list): #may use isinstance(target, Point)
			self._release_point(target)
		else:
			self._release_none()

	def _release_object(self, target_object):
		pass

	def _release_point(self, target_point):
		pass

	def _release_none(self):
		pass


	@classmethod
	def sample(self):
		return Skill(parent=Object.sample(), shape=Shape.sample(), route=Route.sample())

	@classmethod
	def test(self):
		skill = self.sample()
		skill.release()
		#event.bind(('TIME_EVENT', 'TIMER'), skill.step)