#-*- coding:utf-8 -*-

def testmethod(fun):
	def run(self, *args, **kwargs):
		print '%s: INIT' % self.__name__
		result = fun(self, *args, **kwargs)
		print '%s: DESTROY' % self.__name__
		print
		return result
	run = classmethod(run)
	return run