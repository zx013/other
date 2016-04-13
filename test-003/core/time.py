#-*- coding:utf-8 -*-
import time
import itertools

#时间，单位都为毫秒，sleep最小支持1ms，误差1-2%
class Time:
	#间隔，每次运行时间
	interval = 10

	#频率，每秒运行次数
	frequency = 1000 / interval

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
		return t / Time.frequency