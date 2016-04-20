#-*- coding:utf-8 -*-

class Base(object):
	def __init__(self, **kwargs):
	
	def _wrap_event(self, func):
		@wraps
		def run(*args, **kwargs):
			signal(('FUNCTION_EVENT', func.func_name, 'before'), *args, **kwargs)
			result = func(*args, **kwargs)
			result = signal(('FUNCTION_EVENT', func.func_name, 'after'), result, *args, **kwargs)
			return result
		return run

	#在函数前后绑定事件
	def wrap_event(self):
		for key, attr in vars(self).items():
			if not hasattr(attr, '__call__'):
				continue
			attr = self._wrap_event(attr)