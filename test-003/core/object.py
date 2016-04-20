#-*- coding:utf-8 -*-
from core.battle.move.geometry import Coordinate
from core.battle.move.shape import Shape
from core.battle.move.route import Route
from core.battle.buff import Buff, BuffPool
from core.clock import Clock
from core.event import trigger


#ÿ��ʱ��Ƭ�����ͼ��������ײ������ԣ��������а����ƶ�Buff�����壩
#ÿ�������ƶ�ʱ����ײֱ�ӻ�ȡ�����������ײ�����������壩
class BuffMove(Buff):
	'''
		���Ź켣�ƶ�
	'''
	def __init__(self, object, **kwargs):
		Buff.__init__(self, **kwargs)

		self.event = ('TIME_EVENT', 'TIMER')

		#buff���ڵ�object��skill
		self.object = object

	#���·��
	def add_route(self, route):
		self.del_route()
		self.object.route = route
		#self.adjust_to_map()
		trigger(self.event, self.run, self.object.route.move())

	#�Ƴ�·��
	def del_route(self):
		trigger(self.event, self.run)

	#����ת�����ƶ�
	#��ת��ʱ�䲻��һ��ʱ��Ƭ���ۼƣ�ֱ����һ��ʱ��Ƭ����ʱ���м�ʱ
	#�ڹ켣���ƶ�ʱ�������ʱ�仯
	def turn(self, rotate1, rotate2):
		self.object.set_rotate(rotate2)

	def move(self, offset1, offset2):
		self.object.set_offset(offset2)

	def collide(self, frame):
		return []

	#������һ����
	#�ƶ�����һ����
	#������ײ
	def run(self, step):
		collide = self.collide(step['frame'])
		for object in collide:
			object.buffpool += self.object.collide_change
			self.object.buffpool += object.collide_change
		if self.object.across or not collide:
			self.turn(self.object.rotate, step['rotate'])
			self.move(self.object.offset, step['end'])

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

		#���棬�����ƶ�ʱ�Ƿ�������嶯̬����ʵʱ����λ�ã��繳��
		#self.follow = kwargs.get('follow', False)

		#��ײʱ�ܷ񴩹�
		self.across = kwargs.get('across', False)

		#��ײ�����ײ������ʩ�ӵ�buff
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