#-*- coding:utf-8 -*-
__version__ = '1.9.0'
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label


import jnius_config
jnius_config.add_classpath('.', 'paydemoactivity.jar')
from jnius import autoclass

def test():
	Stack = autoclass('java.util.Stack')
	stack = Stack()
	stack.push('hello')
	stack.push('world')
	stack.pop()

def pay(*args):
	PayDemoActivity = autoclass('com.alipay.sdk.pay.demo.PayDemoActivity')
	s = str(PayDemoActivity) + '\n'
	try:
		demo = PayDemoActivity()
	except Exception, ex:
		s += str(ex) + '\n'
	try:
		demo.pay()
	except Exception, ex:
		s += str(ex) + '\n'
	return s


class mainApp(App):
	def build(self):
		test()
		s = pay()
		label = Label(text=s)
		
		return label

if __name__ == '__main__':
	mainApp().run()
