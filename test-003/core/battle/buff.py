#-*- coding:utf-8 -*-
from core.event import trigger, untrigger
from core.tools import Unit

#�ı�object��״̬
#event������buff���¼�
#run��buff��Ч�Ķ�����Ϊ��������ÿһ�δ���ִ��һ�Σ���Ȼ��������raise�˳�
class Buff(Unit):
	def __init__(self, **kwargs):
		#buff���ڵ�object��skill
		pass


	#��ȡ��ǰobject��ʩ��buff��object������object�б�skill���ǵķ�Χ�����м�ֵvalue�����ݹ���object�������ֵ��
	#source_object, target_object

	def create(self):
		trigger(self.event, self.run)

	def destroy(self):
		untrigger(self.event, self.run)

	@classmethod
	def sample(self):
		return Buff()

