#-*- coding:utf-8 -*-

class Event(object):
	def __init__(self, **kwargs):
		self.event = {}

	def signal(self, e, *args, **kwargs):
		for func in self.event.get(e, []):
			if hasattr(func, '__call__'):
				func(*args, **kwargs)
	
	def bind(self, e, func):
		self.event.setdefault(e, [])
		self.event[e].append(func)
	
	@classmethod
	def test(self):
		def fun1(**kwargs):
			print 'fun1', kwargs
		event.bind(('EVENT', 'fun1'), fun1)
		event.signal(('EVENT', 'fun1'), a=1, b=2)
		
		@signal(('EVENT', 'fun2'), False)
		def fun2(**kwargs):
			print 'fun2', kwargs
		
		@bind(('EVENT', 'fun2'))
		def fun3(**kwargs):
			print 'fun3', kwargs
		
		fun2(a=1, b=2, c=3)
			
		
event = Event()

#生成事件
def signal(e, before=True):
	def _signal(func):
		def __signal(*args, **kwargs):
			if before:
				result = event.signal(e, *args, **kwargs)
				func(*args, **kwargs)
			else:
				func(*args, **kwargs)
				result = event.signal(e, *args, **kwargs)
			return result
		return __signal
	return _signal

#绑定事件
def bind(e):
	def _bind(func):
		event.bind(e, func)
		def __bind(*args, **kwargs):
			return func(*args, **kwargs)
		return __bind
	return _bind