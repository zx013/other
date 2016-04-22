#-*- coding:utf-8 -*-
from core.event import trigger, untrigger

#�ı�object��״̬
#event������buff���¼�
#run��buff��Ч�Ķ�����Ϊ��������ÿһ�δ���ִ��һ�Σ���Ȼ��������raise�˳�
class Buff(object):
	def __init__(self, **kwargs):
		#buff���ڵ�object��skill
		self.source_object = kwargs['source_object']

		self.target_object = kwargs.get('target_object')

	#�������Ƿ���object��
	def check(self, var):
		for v in var:
			hasattr(self.source_object, v)
			hasattr(self.target_object, v)

	#��ȡ��ǰobject��ʩ��buff��object������object�б�skill���ǵķ�Χ�����м�ֵvalue�����ݹ���object�������ֵ��
	#source_object, target_object
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
