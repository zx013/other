#-*- coding:utf-8 -*-
from core.battle.move.shape import Shape
from core.battle.move.route import Route
from core.object import Object

class Skill(object):
	def __init__(self, **kwargs):
		self.object = kwargs['object']

		self.shape = kwargs['shape']

		self.route = kwargs['route']

		#跟随，技能移动时是否根据物体动态坐标实时计算位置，如钩子
		self.follow = kwargs.get('follow', False)

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

	def set_adjust(self):
		self.shape.set_offset(self.object.offset)
		self.shape.set_rotate(self.object.rotate)
		self.route.set_offset(self.object.offset)
		self.route.set_rotate(self.object.rotate)

	def run(self):
		self.set_adjust()
		generator = self.route.move()
		for point_list in generator:
			print point_list
			if self.follow:
				self.set_adjust()

	@classmethod
	def test(self):
		skill = Skill(object=Object.sample(), shape=Shape.sample(), route=Route.sample())
		skill.release()
		skill.run()