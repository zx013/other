#-*- coding:utf-8 -*-
import jnius_config
jnius_config.add_classpath('.', 'paydemoactivity.jar')
from jnius import autoclass
context = autoclass('org.renpy.android.PythonActivity').mActivity  


def test():
	Stack = autoclass('java.util.Stack')
	stack = Stack()
	stack.push('hello')
	stack.push('world')
	stack.pop()

def pay():
	PayDemoActivity = autoclass('com.alipay.sdk.pay.demo.PayDemoActivity')
	FragmentActivity = autoclass('android.support.v4.app.FragmentActivity')

	s = str(PayDemoActivity) + '\n'
	try:
		demo = PayDemoActivity(context)
	except Exception, ex:
		s += str(ex) + '\n'

	try:
		fa = FragmentActivity(context)
	except Exception, ex:
		s += str(ex) + '\n'

	try:
		demo.pay()
	except Exception, ex:
		s += str(ex) + '\n'
	return s