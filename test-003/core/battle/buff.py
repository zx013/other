#-*- coding:utf-8 -*-
from core.event import trigger, untrigger

#改变object的状态
#event，触发buff的事件
#run，buff生效的动作，为生成器，每一次触发执行一段，自然结束或用raise退出
class Buff(object):
	def __init__(self, **kwargs):
		#buff所在的object或skill
		self.source_object = kwargs['source_object']

		self.target_object = kwargs.get('target_object')

	#检查变量是否在object中
	def check(self, var):
		for v in var:
			hasattr(self.source_object, v)
			hasattr(self.target_object, v)

	#获取当前object，施加buff的object，关联object列表（skill覆盖的范围），中间值value（根据关联object计算出的值）
	#source_object, target_object
	def info(self):
		pass

	def create(self):
		trigger(self.event, self.run)

	def destroy(self):
		untrigger(self.event, self.run)


#buff的集合，包含若干buff
class BuffPool(object):
	def __init__(self, **kwargs):
		self.buffpool = []

	def insert(self, buff):
		self.buffpool.append(buff)

	def delete(self, buff):
		pass

	def __iadd__(self, other):
		self.buffpool += other.buffpool
