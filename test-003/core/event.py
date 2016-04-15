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

	def unbind(self, e, func):
		if func in self.event[e]:
			self.event[e].remove(func)
	
	@classmethod
	def test(self):
		def fun(**kwargs):
			print 'fun', kwargs
		event.bind(('EVENT', 'fun'), fun)
		event.signal(('EVENT', 'fun'), a=1, b=2)
		
		event.unbind(('EVENT', 'fun'), fun)
		event.signal(('EVENT', 'fun'), a=1, b=2)
			
		
event = Event()

signal = event.signal
bind = event.bind
unbind = event.unbind