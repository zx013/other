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
		if func not in self.event[e]: #同一个函数只能触发一次事件
			self.event[e].append(func)

	def unbind(self, e, func):
		if func in self.event[e]:
			self.event[e].remove(func)

	#将生成器绑定到事件，每次事件触发时调用一次生成器，直到结束
	def trigger(self, e, func):
		generator = func()
		def _trigger(*args, **kwargs):
			try:
				generator.next()
			except:
				self.unbind(e, _trigger)
		self.bind(e, _trigger)
		self.trig[func] = _trigger
	
	def untrigger(self, e, func):
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

		trigger(('EVENT', 'fun'), lambda : (i for i in xrange(2)))
		signal(('EVENT', 'fun'))
		untrigger(('EVENT', 'fun'), fun)
		signal(('EVENT', 'fun'))
		signal(('EVENT', 'fun'))
			
		
event = Event()

signal = event.signal
bind = event.bind
unbind = event.unbind
trigger = event.trigger
untrigger = event.untrigger