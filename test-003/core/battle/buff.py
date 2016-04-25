#-*- coding:utf-8 -*-
from core.event import trigger, untrigger

from copy import copy

#改变object的状态
#event，触发buff的事件
#run，buff生效的动作，为生成器，每一次触发执行一段，自然结束或用raise退出
class Buff(object):
	def __init__(self, **kwargs):
		#buff所在的object或skill
		pass

	#检查变量是否在object中
	def check(self, var):
		for v in var:
			hasattr(self.source_object, v)
			hasattr(self.target_object, v)

	#获取当前object，施加buff的object，关联object列表（skill覆盖的范围），中间值value（根据关联object计算出的值）
	#source_object, target_object

	#创建一个实例
	def action(self, source_object, target_object):
		buff = copy(self)
		buff.source_object = source_object
		buff.target_object = target_object
		return buff

	def create(self):
		trigger(self.event, self.run)

	def destroy(self):
		untrigger(self.event, self.run)

	@classmethod
	def sample(self):
		return Buff()


#buff的集合，包含若干buff
#初始化buffpool，添加到collide_change
#collide_change实例化并添加到另一个已经实例化的buffpool
class BuffPool(object):
	def __init__(self, **kwargs):
		self.buffpool = []

	def insert(self, buff):
		self.buffpool.append(buff)

	def delete(self, buff):
		pass

	def add(self, other, source_object, target_object):
		for buff in other.buffpool:
			self.insert(buff.action(source_object, target_object))
		return self

	@classmethod
	def sample(self):
		return BuffPool()

	@classmethod
	def test(self):
		buffpool1 = BuffPool.sample()
		buffpool2 = BuffPool.sample()

		buff1 = Buff.sample()
		buffpool1.insert(buff1)
		buff2 = Buff.sample()
		buffpool1.insert(buff2)
		buff3 = Buff.sample()
		buffpool2.insert(buff3)
		buff4 = Buff.sample()
		buffpool2.insert(buff4)
		print buffpool1.buffpool, buffpool2.buffpool
