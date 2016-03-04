#-*- coding:utf-8 -*-
import jnius_config
jnius_config.add_classpath('.', 'paydemoactivity.jar')
from jnius import autoclass, cast
from toast import toast

PayTask = autoclass('com.alipay.sdk.app.PayTask')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
Class = autoclass('java.lang.Class')
Bundle = autoclass('android.os.Bundle')
String = autoclass('java.lang.String')


def test():
	Stack = autoclass('java.util.Stack')
	stack = Stack()
	stack.push('hello')
	stack.push('world')
	stack.pop()

def h5pay():
	#AndroidManifest.xml
	#<activity android:name="com.alipay.sdk.pay.demo.H5PayDemoActivity" />
	#.buildozer/android/platform/python-for-android/dist/myapp/templates/AndroidManifest.tmpl.xml
	current = cast('android.app.Activity', PythonActivity.mActivity)
	H5PayDemoActivity = autoclass('com.alipay.sdk.pay.demo.H5PayDemoActivity')
	s = ''
	try:
		intent = Intent(current, Class.forName('com.alipay.sdk.pay.demo.H5PayDemoActivity'))
		extras = Bundle()
		url = String("http://m.taobao.com")
		extras.putString("url", url)
		intent.putExtras(extras)
		current.startActivity(intent)
	except Exception, ex:
		s += str(ex) + '\n'
	l = len(s) / 2
	s = s[:l] + '\n' + s[l:]
	return s

def pay():
	PayDemoActivity = autoclass('com.alipay.sdk.pay.demo.PayDemoActivity')
	FragmentActivity = autoclass('android.support.v4.app.FragmentActivity')

	s = str(PayDemoActivity) + '\n'
	try:
		intent = Intent()
		intent.setAction(Intent.ACTION_VIEW)
		intent.setData(Uri.parse('http://kivy.org'))
		#cls = Class.forName('com.alipay.sdk.pay.demo.PayDemoActivity')
		#intent.setClass(PythonActivity.mActivity, cls)
	except Exception, ex:
		s += str(ex) + '\n'

	try:
		#demo = PayDemoActivity()
		currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
		currentActivity.startActivity(intent)
	except Exception, ex:
		s += str(ex) + '\n'

	return s

def pay_test():
	test()
	s = h5pay()
	toast('abc')
	return s