#-*- coding:utf-8 -*-
from core.battle.move.route import Route
from core.battle.buff import Buff
from core.tools import Tools, Pool


#操作详细流程
#创建object
#object添加到地图

#object创建skill
#skill添加到地图

#定义buff类
#创建buff
#buff添加到skill.collide_buffpool
#创建movebuff
#movebuff添加到skill.buffpool
#运行movebuff

#skill和object碰撞
#skill.collide_buffpool添加到object.buffpool
#buff生效并运行


#API流程

#class Objectxxx: pass #定义一个object，包含skill
#位置offset，方向rorate，形状shape

#class Skillxxx: pass #定义一个skill，包含buff
#位置offset，方向rorate，形状shape，轨迹route

#class Buffxxx: pass #定义一个buff
#源object，目标object，变量value
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


#每个时间片计算地图中所有碰撞的物体对（计算所有包含移动Buff的物体）
#每个物体移动时的碰撞直接获取结果（物体碰撞到的其它物体）
class BuffMove(Buff):
	#改变rotate, offset
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
	#一个时间片的移动（旋转）
	def run(self):
		#状态和下一个状态，#给map计算碰撞
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