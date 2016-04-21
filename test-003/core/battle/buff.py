#-*- coding:utf-8 -*-
from core.event import trigger, untrigger

#�ı�object��״̬
#event������buff���¼�
#run��buff��Ч�Ķ�����Ϊ��������ÿһ�δ���ִ��һ�Σ���Ȼ��������raise�˳�
class Buff(object):
	def __init__(self, **kwargs):
		pass
	
	#��ȡ��ǰobject��ʩ��buff��object������object�б�
	def info(self):
		pass

	def create(self):
		trigger(self.event, self.run)

	def destroy(self):
		untrigger(self.event, self.run)


#buff�ļ��ϣ���������buff
class BuffPool(object):
	def __init__(self, **kwargs):
		self.buffpool = []

	def insert(self, buff):
		self.buffpool.append(buff)

	def delete(self, buff):
		pass

	def __iadd__(self, other):
		self.buffpool += other.buffpool
