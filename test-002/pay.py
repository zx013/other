#-*- coding:utf-8 -*-

import jnius_config
jnius_config.add_classpath('.', 'paydemoactivity.jar')


from kivy.logger import Logger
from jnius import autoclass, PythonJavaClass, java_method, cast
from android import activity
from android.runnable import run_on_ui_thread

Toast = autoclass('android.widget.Toast')
context = autoclass('org.renpy.android.PythonActivity').mActivity    

@run_on_ui_thread
def toast(text, length_long=False):
    duration = Toast.LENGTH_LONG if length_long else Toast.LENGTH_SHORT
    String = autoclass('java.lang.String')
    c = cast('java.lang.CharSequence', String(text))
    t = Toast.makeText(context, c, duration)
    t.show()



def test():
	Stack = autoclass('java.util.Stack')
	stack = Stack()
	stack.push('hello')
	stack.push('world')
	stack.pop()

def pay(*args):
	PayDemoActivity = autoclass('com.alipay.sdk.pay.demo.PayDemoActivity')
	FragmentActivity = autoclass('android.support.v4.app.FragmentActivity')
	activity = autoclass('org.renpy.android.PythonActivity').mActivity

	s = str(PayDemoActivity) + '\n'
	try:
		demo = PayDemoActivity()
	except Exception, ex:
		s += str(ex) + '\n'

	try:
		fa = FragmentActivity()
	except Exception, ex:
		s += str(ex) + '\n'

	try:
		demo.pay()
	except Exception, ex:
		s += str(ex) + '\n'
	return s