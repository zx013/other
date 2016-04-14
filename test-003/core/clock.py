#-*- coding:utf-8 -*-
import time
import itertools
import thread
from core.event import event, signal

#时间，单位都为毫秒，sleep最小支持1ms，误差1-2%
class Clock(object):
	#间隔，每次运行时间
	interval = 10

	#频率，每秒运行次数
	frequency = 1000 / interval

	@staticmethod
	def timer():
		def _timer():
			while 1:
				event.signal(('TIME_EVENT', 'TIMER'))
				Clock.sleep(Clock.interval)
		thread.start_new_thread(_timer, ())

	@staticmethod
	def clock():
		return int(time.time() * 1000)

	@staticmethod
	def sleep(tm):
		time.sleep(tm / 1000.0)

	@staticmethod
	def through():
		return itertools.count(0)

	#普通时间转换为时间片
	@staticmethod
	def convert_frequency(t):
		return t / Clock.frequency

	@classmethod
	def test(self):
		Clock.clock()
		Clock.sleep(100)
		Clock.timer()