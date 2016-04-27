#-*- coding:utf-8 -*-
from core.event import trigger, untrigger
from core.tools import Unit

#�ı�object��״̬
#event������buff���¼�
#run��buff��Ч�Ķ�����Ϊ��������ÿһ�δ���ִ��һ�Σ���Ȼ��������raise�˳�
class Buff(Unit):
	def __init__(self, **kwargs):
		Unit.__init__(self, **kwargs)


	#��ȡ��ǰobject��ʩ��buff��object������object�б�skill���ǵķ�Χ�����м�ֵvalue�����ݹ���object�������ֵ��
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

