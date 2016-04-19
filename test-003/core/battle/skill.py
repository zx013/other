#-*- coding:utf-8 -*-
from core.battle.move.shape import Shape
from core.battle.move.route import Route
from core.battle.buff import Buff, BuffPool
from core.object import Object
from core.clock import Clock
from core.event import trigger


#ÿ��ʱ��Ƭ�����ͼ��������ײ������ԣ��������а����ƶ�Buff�����壩
#ÿ�������ƶ�ʱ����ײֱ�ӻ�ȡ�����������ײ�����������壩
class BuffMove(Buff):
	'''
		���Ź켣�ƶ�
	'''
	def __init__(self, object, **kwargs):
		print 'abc'
		Buff.__init__(self, **kwargs)

		self.event = ('TIME_EVENT', 'TIMER')
		
		#buff���ڵ�object��skill
		self.object = object

		self.map_adjust()
		trigger(self.event, self.run, self.object.route.move())

	#����ת�����ƶ�
	#��ת��ʱ�䲻��һ��ʱ��Ƭ���ۼƣ�ֱ����һ��ʱ��Ƭ����ʱ���м�ʱ
	#�ڹ켣���ƶ�ʱ�������ʱ�仯
	def turn(self, rotate1, rotate2):
		self.object.set_rotate(rotate2)

	def pre_move(self):
		pass

	def move(self, offset1, offset2):
		self.object.set_offset(offset2)

	def step(self, step):
		print 'step', step
		self.turn(self.object.rotate, step['direct'])
		self.move(self.object.offset, step['end'])
		#trigger(self.event, self.run)

	def collide(self):
		return []

	#������һ����
	#�ƶ�����һ����
	#������ײ
	def run(self, step):
		collide = self.collide()
		for object in collide:
			object.buffpool += self.object.collide_change
			self.object.buffpool += object.collide_change
		if self.object.across or not collide:
			self.step(step)

	#�������������ͼ����
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

		#���棬�����ƶ�ʱ�Ƿ�������嶯̬����ʵʱ����λ�ã��繳��
		#self.follow = kwargs.get('follow', False)
		
		#��ײʱ�ܷ񴩹�
		self.across = kwargs.get('across', False)

		self.buffpool.insert(BuffMove(self))

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
		return Skill(parent=Object.sample(), shape=Shape.sample(), route=Route.sample())

	@classmethod
	def test(self):
		skill = self.sample()
		skill.release()