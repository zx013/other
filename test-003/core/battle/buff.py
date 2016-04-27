#-*- coding:utf-8 -*-
from core.event import trigger, untrigger
from core.tools import Unit

#改变object的状态
#event，触发buff的事件
#run，buff生效的动作，为生成器，每一次触发执行一段，自然结束或用raise退出
class Buff(Unit):
	def __init__(self, **kwargs):
		Unit.__init__(self, **kwargs)


	#获取当前object，施加buff的object，关联object列表（skill覆盖的范围），中间值value（根据关联object计算出的值）
	#source_object, target_object

	def action(self, **kwargs):
		unit = Unit.action(self, **kwargs)
		unit.create()
		return unit

	def create(self):
		trigger(self.event, self.run)

	def destroy(self):
		untrigger(self.event, self.run)

	def run(self):
		yield

	@classmethod
	def sample(self):
		return Buff(event=('test',))

