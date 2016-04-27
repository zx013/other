#-*- coding:utf-8 -*-
from core.object import Object
from core.tools import Pool

from core.script.buff.buffmove import BuffMove


#���ݵ�buff���ƶ�·��
class Skill(Object):
	def __init__(self, **kwargs):
		Object.__init__(self, **kwargs)

		self.buffmove = BuffMove()

	def run(self):
		self.buffpool.insert(self.buffmove, route=self.route, source_object=self)
		print self.buffpool.pool, tuple(self.buffpool.pool)[0].source_object

	#Ĭ�ϴ���Ĳ�����source_object
	#ѡ��һ��Ŀ�꣬target_object
	#ѡ��һ���㣬target_point
	#��
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
		from core.battle.move.route import Route
		return Skill(route=Route.sample())

	@classmethod
	def test(self):
		skill = Skill.sample()
		skill.release()
		skill.run()
