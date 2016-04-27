#-*- coding:utf-8 -*-
from core.battle.buff import Buff
from core.tools import Tools, Pool


#操作者直接进行操作
#该操作后台具体执行流程
#将可量化和计算方法作为脚本


#A使用技能B攻击C
#创建A，C
#在A中创建B的模版（开局）

#A使用技能B（操作）
#生成B的轨迹（根据点击的位置计算，计算方法事先定义）
#实例化B（使用轨迹）
#B沿轨迹运行

#全地图碰撞，生成地图碰撞事件（响应时钟事件）
#B碰撞C（响应地图碰撞事件）
#实例化B的碰撞buff（使用B，C以及附加值）
#将B的碰撞buff传递给C

#buff生效（响应事件）



#初始化时生成模版
#之后根据action函数实例化，添入其它空缺参数
#比如类A有a, b, c三个参数
#a = A(a=1)，初始化模板，固定参数a
#a.action(b=2, c=3)，实例化时，只需传入初始化未传入的参数

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
