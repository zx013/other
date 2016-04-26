#-*- coding:utf-8 -*-
from core.battle.move.route import Route
from core.battle.buff import Buff
from core.tools import Tools, Pool


#������ϸ����
#����object
#object��ӵ���ͼ

#object����skill
#skill��ӵ���ͼ

#����buff��
#����buff
#buff��ӵ�skill.collide_buffpool
#����movebuff
#movebuff��ӵ�skill.buffpool
#����movebuff

#skill��object��ײ
#skill.collide_buffpool��ӵ�object.buffpool
#buff��Ч������


#API����

#class Objectxxx: pass #����һ��object������skill
#λ��offset������rorate����״shape

#class Skillxxx: pass #����һ��skill������buff
#λ��offset������rorate����״shape���켣route

#class Buffxxx: pass #����һ��buff
#Դobject��Ŀ��object������value
#
#

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
		from core.object import Object
		return BuffAttack(source_object=Object.sample(), target_object=Object.sample())

	@classmethod
	def test(self):
		buffattack = BuffAttack.sample()
		#buffattack.create()


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
		return BuffMove(route=Route.sample())

	@classmethod
	def test(self):
		from core.object import Object
		buffmove = BuffMove.sample()
		buffmove = buffmove.action(source_object=Object.sample(), target_object=Object.sample())
		#buffmove.create()



from core.battle.skill import Skill

class SkillMove(Skill):
	def __init__(self, **kwargs):
		Skill.__init__(self, **kwargs)

		self.buffpool = Pool()

	@classmethod
	def sample(self):
		return SkillMove()


from core.object import Object

class ObjectOperate(Object):
	def __init__(self, **kwargs):
		Object.__init__(self, **kwargs)
		
		self.skillpool = Pool()
	
	@classmethod
	def sample(self):
		return ObjectOperate()