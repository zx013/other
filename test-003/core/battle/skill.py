#-*- coding:utf-8 -*-
from core.battle.move.shape import Shape
from core.battle.move.route import Route
from core.battle.buff import Buff, BuffPool
from core.object import Object
from core.event import event, bind

class BuffMove(Buff):
	def __init__(self, skill, **kwargs):
		Buff.__init__(self, **kwargs)
		self.skill = skill
		self.object = self.skill.object
		self.shape = self.skill.shape
		self.route = self.skill.route
		

	def run(self):
		pass

	def next(self):
		pass

	def move_adjust(self):
		self.shape.set_offset(self.object.offset)
		self.shape.set_rotate(self.object.rotate)
		self.route.set_offset(self.object.offset)
		self.route.set_rotate(self.object.rotate)

	def move(self):
		self.move_adjust()
		generator = self.route.move()
		for point_list in generator:
			yield point_list
			if self.follow:
				self.move_adjust()


class Skill(object):
	def __init__(self, **kwargs):
		self.object = kwargs['object']

		self.shape = kwargs['shape']

		self.route = kwargs['route']
		
		self.buffpool = BuffPool()

		#跟随，技能移动时是否根据物体动态坐标实时计算位置，如钩子
		self.follow = kwargs.get('follow', False)

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


	@staticmethod
	@bind(('TIME_EVENT', 'TIMER'))
	def step():
		#print 'abc%sabc' % str(self.g.next())
		print 'abc'

	@classmethod
	def sample(self):
		return Skill(object=Object.sample(), shape=Shape.sample(), route=Route.sample())

	@classmethod
	def test(self):
		skill = self.sample()
		skill.release()
		print event.event
		#event.bind(('TIME_EVENT', 'TIMER'), skill.step)