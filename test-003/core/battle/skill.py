#-*- coding:utf-8 -*-
from core.object import Object
from core.tools import Pool

from core.script.buff.buffmove import BuffMove


#传递的buff，移动路径
class Skill(Object):
	def __init__(self, **kwargs):
		Object.__init__(self, **kwargs)

		self.buffmove = BuffMove()

	def run(self):
		self.buffpool.insert(self.buffmove, route=self.route, source_object=self)
		print self.buffpool.pool, tuple(self.buffpool.pool)[0].source_object

	#三种释放方式
	#无须选择，直接使用
	#选择目标object
	#选择目标点
	def release(self, target=None):
		if isinstance(target, Object):
			self._release_object(target)
		elif isinstance(target, tuple) or isinstance(target, list): #may use isinstance(target, Point)
			self._release_point(target)
		else:
			self._release_none()

	#一个时间片（关联自身和目标），追踪路径
	def _release_object(self, target_object):
		pass

	#直线轨迹
	def _release_point(self, target_point):
		pass

	#一个时间片（关联自身），扩张动作
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
		#skill.run()
