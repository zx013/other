#-*- coding:utf-8 -*-

class Event(object):
	def __init__(self, **kwargs):
		self.event = {}
		self.trig = {}

	def signal(self, e, *args, **kwargs):
		for func in self.event.get(e, []):
			if hasattr(func, '__call__'):
				func(*args, **kwargs)
	
	def bind(self, e, func):
		self.event.setdefault(e, [])
		self.event[e].append(func)

	def unbind(self, e, func):
		if func in self.event[e]:
			self.event[e].remove(func)

	#将生成器绑定到事件，每次事件触发时调用一次生成器作为函数参数，直到结束
	def trigger(self, e, func, generator=None):
		def _trigger(*args, **kwargs):
			try:
				func(generator.next())
			except:
				self.unbind(e, _trigger)
		if generator:
			self.bind(e, _trigger)
			self.trig[func] = _trigger
		else:
			if self.trig.get(func):
				self.unbind(e, self.trig[func])
				del self.trig[func]
	
	@classmethod
	def test(self):
		def fun(*args, **kwargs):
			print 'fun', args, kwargs
		bind(('EVENT', 'fun'), fun)
		signal(('EVENT', 'fun'), a=1, b=2)
		
		unbind(('EVENT', 'fun'), fun)
		signal(('EVENT', 'fun'), a=1, b=2)

		trigger(('EVENT', 'fun'), fun, (i for i in xrange(2)))
		signal(('EVENT', 'fun'))
		trigger(('EVENT', 'fun'), fun)
		signal(('EVENT', 'fun'))
		signal(('EVENT', 'fun'))
			
		
event = Event()

signal = event.signal
bind = event.bind
unbind = event.unbind
trigger = event.trigger
