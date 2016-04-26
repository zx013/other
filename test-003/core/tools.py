#-*- coding:utf-8 -*-
import itertools

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


class Tools(object):
	#��0��ʼ����
	@staticmethod
	def count():
		return itertools.count(0)

	#ѭ����0��С��0ʱ����ѭ��
	@staticmethod
	def repeat(cycle):
		if cycle <= 0:
			return itertools.repeat(0)
		else:
			return itertools.repeat(0, cycle)

	#(0, 1, 2, 3, 4)
	#(None, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, None)
	@staticmethod
	def future(generator):
		v1 = None
		for v2 in generator:
			yield v1, v2
			v1 = v2
		yield v1, None


from copy import copy

class Unit(object):
	def check(self, var):
		for v in var:
			hasattr(self.source_object, v)
			hasattr(self.target_object, v)

	#����һ��ʵ��
	def action(self, **kwargs):
		unit = copy(self)
		for key, value in kwargs.items():
			setattr(unit, key, value)
		return unit

	@classmethod
	def sample(self):
		return Unit()


class Pool(object):
	def __init__(self, **kwargs):
		self.pool = set()

	#���ж��������ʵ����
	def insert(self, unit, **kwargs):
		if not kwargs:
			self.pool.add(unit)
		else:
			self.pool.add(unit.action(**kwargs))

	def delete(self, unit):
		if unit in self.pool:
			self.pool.remove(unit)

	def add(self, pool, **kwargs):
		for unit in pool.pool:
			self.insert(unit, **kwargs)

	def loop(self, cmp=None, key=None, reverse=False):
		return sorted(self.pool, cmp, key, reverse)

	@classmethod
	def sample(self):
		return Pool()

	@classmethod
	def test(self):
		unitpool1 = Pool.sample()
		unitpool2 = Pool.sample()

		unit1 = Unit.sample()
		unitpool1.insert(unit1)
		unit2 = Unit.sample()
		unitpool1.insert(unit2)
		unit3 = Unit.sample()
		unitpool2.insert(unit3)
		unit4 = Unit.sample()
		unitpool2.insert(unit4)
		print unitpool1.pool, unitpool2.pool