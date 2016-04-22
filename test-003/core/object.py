#-*- coding:utf-8 -*-
from core.battle.move.geometry import Coordinate
from core.battle.move.shape import Shape
from core.battle.move.route import Route
from core.battle.buff import Buff, BuffPool
from core.tools import Tools
from core.clock import Clock


class BuffAttack(Buff):
	def __init__(self, **kwargs):
		Buff.__init__(self, **kwargs)

		self.event = ('TIME_EVENT', 'TIMER')

		self.var = ['life', 'attack', 'defense']

	def run(self):
		damage = self.source_object.attack - self.target_object.defense
		self.target_object.life -= damage
		print self.source_object.life, self.target_object.life
		yield


	@classmethod
	def sample(self):
		return BuffAttack(source_object=Object.sample(), target_object=Object.sample())

	@classmethod
	def test(self):
		buffattack = BuffAttack.sample()
		buffattack.create()


#ÿ��ʱ��Ƭ�����ͼ��������ײ������ԣ��������а����ƶ�Buff�����壩
#ÿ�������ƶ�ʱ����ײֱ�ӻ�ȡ�����������ײ�����������壩
class BuffMove(Buff):
	#�ı�rotate, offset
	def __init__(self, **kwargs):
		Buff.__init__(self, **kwargs)

		self.event = ('MAP_EVENT', 'COLLIDE')

		self.route = kwargs['route']

	def turn(self, rotate1, rotate2):
		self.source_object.set_rotate(rotate2)

	def move(self, offset1, offset2):
		self.source_object.set_offset(offset2)

	def collide(self):
		return

	#{'start': (1.5, 9.184850993605148e-17), 'frame': [(2.0, 1.2246467991473532e-16)], 'end': (2.0, 1.2246467991473532e-16), 'type': 'move'}
	#{'start': 90.0, 'end': 70.0, 'type': 'rotate'}
	#һ��ʱ��Ƭ���ƶ�����ת��
	def run(self):
		#״̬����һ��״̬��#��map������ײ
		for state, future in Tools.future(self.route.move()):
			self.future = future
			if state is None:
				continue
			print state
			if state['type'] == 'rotate':
				self.turn(state['start'], state['end'])
			elif state['type'] == 'move':
				if not self.source_object.across and self.collide():
					raise
				self.move(state['start'], state['end'])
			yield

	@classmethod
	def sample(self):
		return BuffMove(source_object=Object.sample(), route=Route.sample())

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

		#���棬�����ƶ�ʱ�Ƿ�������嶯̬����ʵʱ����λ�ã��繳��
		#self.follow = kwargs.get('follow', False)

		#��ײʱ�ܷ񴩹�
		self.across = kwargs.get('across', False)

		#��ײ�����ײ������ʩ�ӵ�buff
		self.collide_change = BuffPool()

		self.buffpool = BuffPool()

		self.buffpool.insert(BuffMove(source_object=self, route=None))


		self.life = 5.0
		self.attack = 2.0
		self.defense = 1.0

	def add(self, shape):
		self.shape = kwargs['shape']

	def select(self, operate):
		pass

	#��ȡ����������
	def get_beside(self):
		return [self]

	@classmethod
	def sample(self):
		return Object()