#-*- coding:utf-8 -*-
from core.event import trigger, untrigger

from copy import copy

#�ı�object��״̬
#event������buff���¼�
#run��buff��Ч�Ķ�����Ϊ��������ÿһ�δ���ִ��һ�Σ���Ȼ��������raise�˳�
class Buff(object):
	def __init__(self, **kwargs):
		#buff���ڵ�object��skill
		pass

	#�������Ƿ���object��
	def check(self, var):
		for v in var:
			hasattr(self.source_object, v)
			hasattr(self.target_object, v)

	#��ȡ��ǰobject��ʩ��buff��object������object�б�skill���ǵķ�Χ�����м�ֵvalue�����ݹ���object�������ֵ��
	#source_object, target_object

	#����һ��ʵ��
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


#buff�ļ��ϣ���������buff
#��ʼ��buffpool����ӵ�collide_change
#collide_changeʵ��������ӵ���һ���Ѿ�ʵ������buffpool
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
