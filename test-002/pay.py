#-*- coding:utf-8 -*-
import jnius_config
jnius_config.add_classpath('.', 'paydemoactivity.jar')
from jnius import autoclass, cast
from toast import toast

PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
Class = autoclass('java.lang.Class')
Bundle = autoclass('android.os.Bundle')
String = autoclass('java.lang.String')


current = cast('android.app.Activity', PythonActivity.mActivity)

def test():
	Stack = autoclass('java.util.Stack')
	stack = Stack()
	stack.push('hello')
	stack.push('world')
	stack.pop()

#AndroidManifest.xml
#<uses-permission android:name="android.permission.INTERNET" />
#<activity android:name="com.alipay.sdk.pay.demo.H5PayDemoActivity" />
#modify: .buildozer/android/platform/python-for-android/dist/myapp/templates/AndroidManifest.tmpl.xml
#delete: setContentView(R.layout.pay_main);
def h5pay():	
	H5PayDemoActivity = autoclass('com.alipay.sdk.pay.demo.H5PayDemoActivity')
	s = ''
	try:
		intent = Intent(current, Class.forName('com.alipay.sdk.pay.demo.H5PayDemoActivity'))
		extras = Bundle()
		url = String("http://m.taobao.com")
		extras.putString("url", url)
		intent.putExtras(extras)
		current.startActivityForResult(intent, 0)
	except Exception, ex:
		s += str(ex) + '\n'
	l = len(s) / 2
	s = s[:l] + '\n' + s[l:]
	return s


def pay():
	PayDemoActivity = autoclass('com.alipay.sdk.pay.demo.PayDemoActivity')

	s = str(PayDemoActivity) + '\n'
	try:
		intent = Intent(current, Class.forName('com.alipay.sdk.pay.demo.PayDemoActivity'))
		#intent.setAction(Intent.ACTION_VIEW)
		#intent.setData(Uri.parse('http://kivy.org'))
		current.startActivityForResult(intent, 0)
		#current.h5pay()
	except Exception, ex:
		s += str(ex) + '\n'
	return s

def popup():
	from kivy.uix.popup import Popup
	p = Popup(title='Test popup', size_hint=(None, None), size=(256, 256))
	p.open()

def pay_test():
	test()
	s = pay()
	popup()
	toast('abc')
	return s