#-*- coding:utf-8 -*-
import itertools

#封装的函数为递归式与非递归式，递归式由上一次状态计算得出，非递归式则直接算出
#类成员在使用时会随时间片实时改变，其中改变分为内部或外部改变
#不能够被改变的成员无需改动，直接使用即可
#能够被改变的成员必需封装到lambda中，用函数调用形式使用
#外部改变时，递归式只需改变递归值即可，非递归式则需再次封装一层，两者实现的效果不同
class Iterate(object):
	def __init__(self, func, input=lambda x: x, output=lambda x: x, **kwargs):
		#recurse为递归初值，未设置则视为非递归
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


class Tools:
	#从0开始计数
	@staticmethod
	def count():
		return itertools.count(0)
	
	#循环，0或小于0时无限循环
	@staticmethod
	def repeat(cycle):
		if cycle <= 0:
			return itertools.repeat(0)
		else:
			return itertools.repeat(0, cycle)