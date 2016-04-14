#-*- coding:utf-8 -*-

#��װ�ĺ���Ϊ�ݹ�ʽ��ǵݹ�ʽ���ݹ�ʽ����һ��״̬����ó����ǵݹ�ʽ��ֱ�����
#���Ա��ʹ��ʱ����ʱ��Ƭʵʱ�ı䣬���иı��Ϊ�ڲ����ⲿ�ı�
#���ܹ����ı�ĳ�Ա����Ķ���ֱ��ʹ�ü���
#�ܹ����ı�ĳ�Ա�����װ��lambda�У��ú���������ʽʹ��
#�ⲿ�ı�ʱ���ݹ�ʽֻ��ı�ݹ�ֵ���ɣ��ǵݹ�ʽ�����ٴη�װһ�㣬����ʵ�ֵ�Ч����ͬ
class Iterate(object):
	def __init__(self, func, input=lambda x: x, output=lambda x: x, **kwargs):
		#recurseΪ�ݹ��ֵ��δ��������Ϊ�ǵݹ�
		if kwargs.has_key('recurse'):
			self.recurse = kwargs['recurse']

		if hasattr(func, '__call__'):
			self.func = lambda *args, **kwargs: output(func(input(*args, **kwargs)))
		else:
			self.func = lambda *args, **kwargs: output(func)

	def __call__(self, *args, **kwargs):
		if hasattr(self, 'recurse'):
			self.recurse = self.func(self.recurse, *args, **kwargs)
			return self.recurse
		else:
			return self.func(*args, **kwargs)
	
	@classmethod
	def test(self):
		a1 = Iterate(1, recurse=2)
		print a1(), a1(), a1()
		a2 = Iterate(lambda x: x + 1, recurse=2)
		print a2(), a2(), a2()