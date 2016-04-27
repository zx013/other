#-*- coding:utf-8 -*-
from core.battle.buff import Buff
from core.tools import Tools


#每个时间片计算地图中所有碰撞的物体对（计算所有包含移动Buff的物体）
#每个物体移动时的碰撞直接获取结果（物体碰撞到的其它物体）
class BuffMove(Buff):
	#改变rotate, offset
	def __init__(self, **kwargs):
		Buff.__init__(self, **kwargs)

		self.event = ('MAP_EVENT', 'COLLIDE')

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
		from core.battle.move.route import Route
		return BuffMove(route=Route.sample())

	@classmethod
	def test(self):
		from core.object import Object
		buffmove = BuffMove.sample()
		buffmove = buffmove.action(source_object=Object.sample(), target_object=Object.sample())
		#buffmove.create()
