#-*- coding:utf-8 -*-
import time
import itertools

#ʱ�䣬��λ��Ϊ���룬sleep��С֧��1ms�����1-2%
class Time:
	#�����ÿ������ʱ��
	interval = 10

	#Ƶ�ʣ�ÿ�����д���
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

	#��ͨʱ��ת��Ϊʱ��Ƭ
	@staticmethod
	def convert_frequency(t):
		return t / Time.frequency