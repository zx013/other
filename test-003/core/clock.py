#-*- coding:utf-8 -*-
import time
import thread
from core.event import signal

#ʱ�䣬��λ��Ϊ���룬sleep��С֧��1ms�����1-2%
class Clock(object):
	#�����ÿ������ʱ��
	interval = 10

	#Ƶ�ʣ�ÿ�����д���
	frequency = 1000 / interval

	#��ʱ�����д���
	number = 0
	
	@staticmethod
	def timer():
		def _timer():
			while 1:
				signal(('TIME_EVENT', 'TIMER'))
				Clock.number += 1
				Clock.sleep(Clock.interval)
		thread.start_new_thread(_timer, ())

	#��ʱִ��
	@staticmethod
	def delay(t, func, *args, **kwargs):
		def _delay():
			func(*args, **kwargs)
		Clock.sleep(t)
		thread.start_new_thread(_delay, ())

	@staticmethod
	def clock():
		return int(time.time() * 1000)

	@staticmethod
	def sleep(tm):
		time.sleep(tm / 1000.0)

	#��ͨʱ��ת��Ϊʱ��Ƭ
	@staticmethod
	def convert_frequency(t):
		return t / Clock.frequency

	@classmethod
	def test(self):
		Clock.clock()
		Clock.sleep(100)
		Clock.timer()