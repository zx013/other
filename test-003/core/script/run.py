#-*- coding:utf-8 -*-
from core.battle.buff import Buff
from core.tools import Tools, Pool


#������ֱ�ӽ��в���
#�ò�����̨����ִ������
#���������ͼ��㷽����Ϊ�ű�


#Aʹ�ü���B����C
#����A��C
#��A�д���B��ģ�棨���֣�

#Aʹ�ü���B��������
#����B�Ĺ켣�����ݵ����λ�ü��㣬���㷽�����ȶ��壩
#ʵ����B��ʹ�ù켣��
#B�ع켣����

#ȫ��ͼ��ײ�����ɵ�ͼ��ײ�¼�����Ӧʱ���¼���
#B��ײC����Ӧ��ͼ��ײ�¼���
#ʵ����B����ײbuff��ʹ��B��C�Լ�����ֵ��
#��B����ײbuff���ݸ�C

#buff��Ч����Ӧ�¼���



#��ʼ��ʱ����ģ��
#֮�����action����ʵ����������������ȱ����
#������A��a, b, c��������
#a = A(a=1)����ʼ��ģ�壬�̶�����a
#a.action(b=2, c=3)��ʵ����ʱ��ֻ�贫���ʼ��δ����Ĳ���

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

	@classmethod
	def test(self):
		from core.battle.move.shape import Shape

		object1 = Object.sample()
		object1.shape = Shape.sample()

		object2 = Object.sample()
		object2.shape = Shape.sample()


		skill1 = Skill.sample()
		skill1.shape = Shape.sample()
		object1.add(skill1)

		skill2 = Skill.sample()
		skill2.shape = Shape.sample()
		object2.add(skill2)


		buff1 = Buff.sample()
		buff2 = Buff.sample()
		skill2.collide_buffpool.insert(buff1)
		skill2.collide_buffpool.insert(buff2)

		object1.collide(skill2)


		buff3 = object1.buffpool.pool.pop()
		buff4 = object1.buffpool.pool.pop()
		print type(buff3.source_object), type(buff3.target_object)
