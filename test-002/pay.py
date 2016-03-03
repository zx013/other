#-*- coding:utf-8 -*-
import jnius_config
jnius_config.add_classpath('.', 'paydemoactivity.jar')
from jnius import autoclass, cast

PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')


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
		intent = Intent()
		#intent.setClass(PythonActivity.mActivity, FragmentActivity)
		intent.setAction(Intent.ACTION_VIEW)
		intent.setData(Uri.parse('http://kivy.org'))
	except Exception, ex:
		s += str(ex) + '\n'

	try:
		#demo = PayDemoActivity()
		currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
		currentActivity.startActivity(intent)
	except Exception, ex:
		s += str(ex) + '\n'

	return s