#-*- coding:utf-8 -*-
import jnius_config
jnius_config.add_classpath('.', 'alipaySdk-20160120.jar', 'paydemoactivity.jar')
from jnius import autoclass, cast
from toast import toast

'''
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
Class = autoclass('java.lang.Class')
Bundle = autoclass('android.os.Bundle')
String = autoclass('java.lang.String')

current = cast('android.app.Activity', PythonActivity.mActivity)
'''

def test():
	Stack = autoclass('java.util.Stack')
	stack = Stack()
	stack.push('hello')
	stack.push('world')
	stack.pop()

#AndroidManifest.xml
#<uses-permission android:name='android.permission.INTERNET' />
#<activity android:name='com.alipay.sdk.pay.demo.H5PayDemoActivity' />
#modify: .buildozer/android/platform/python-for-android/dist/myapp/templates/AndroidManifest.tmpl.xml
#delete: setContentView(R.layout.pay_main);
'''
def h5paydemo():
	H5PayDemoActivity = autoclass('com.alipay.sdk.pay.demo.H5PayDemoActivity')
	s = ''
	try:
		intent = Intent(current, Class.forName('com.alipay.sdk.pay.demo.H5PayDemoActivity'))
		extras = Bundle()
		url = String('http://m.taobao.com')
		extras.putString('url', url)
		intent.putExtras(extras)
		current.startActivityForResult(intent, 0)
	except Exception, ex:
		s += str(ex) + '\n'
	l = len(s) / 2
	s = s[:l] + '\n' + s[l:]
	return s


def paydemo():
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
'''


import time
import random
import urllib
import thread

String = autoclass('java.lang.String')
#URLEncoder = autoclass('java.net.URLEncoder')

PayTask = autoclass('com.alipay.sdk.app.PayTask')
SignUtils = autoclass('com.alipay.sdk.pay.demo.SignUtils')


PythonActivity = autoclass('org.renpy.android.PythonActivity')
context = cast('android.app.Activity', PythonActivity.mActivity)


class Pay:
	PARTNER = ''
	SELLER = ''
	RSA_PRIVATE = ''
	RSA_PUBLIC = ''

	def run(self, payInfo):
		#alipay = PayTask(context)
		#result = alipay.pay(payInfo, True)
		thread.exit_thread()

	def pay(self):
		if self.PARTNER == '' or self.RSA_PRIVATE == '' or self.SELLER == '':
			#popup()
			pass
			#return

		orderInfo = self.getOrderInfo('test good', 'test good info', '0.01')
		sign = self.sign(orderInfo)
		try:
			if isinstance(sign, unicode):
				sign = sign.encode('utf-8')
			sign = urllib.quote(sign)
			#sign = URLEncoder.encode(sign, 'UTF-8')
		except Exception, ex:
			pass

		payInfo = '%s&sign="%s"&%s' % (orderInfo, sign, self.getSignType())

		thread.start_new_thread(self.run, (payInfo,))
		alipay = PayTask(context)
		result = alipay.pay(payInfo, True)
		return result

	def getOrderInfo(self, subject, body, price):
		orderInfo = 'partner="%s"' % self.PARTNER
		orderInfo += '&seller_id="%s"' % self.SELLER
		orderInfo += '&out_trade_no="%s"' % self.getOutTradeNo()
		orderInfo += '&subject="%s"' % subject
		orderInfo += '&body="%s"' % body
		orderInfo += '&total_fee="%s"' % price
		orderInfo += '&notify_url="%s"' % 'http://notify.msp.hk/notify.htm'
		orderInfo += '&service="mobile.securitypay.pay"'
		orderInfo += '&payment_type="1"'
		orderInfo += '&_input_charset="utf-8"'
		orderInfo += '&it_b_pay="30m"'
		#orderInfo += '&extern_token="%s"' % extern_token
		orderInfo += '&return_url="m.alipay.com"'
		#orderInfo += '&paymethod="expressGateway"'
		return orderInfo

	def getOutTradeNo(self):
		key = str(int(time.time() * 1000))
		key += str(random.random())[2:]
		key = key[:20]
		return key

	def sign(self, content):
		return SignUtils.sign(content, self.RSA_PRIVATE)

	def getSignType(self):
		return 'sign_type="RSA"'

def pay_test():
	test()
	#s = paydemo()
	s = 'none\n'
	try:
		p = Pay()
		s += str(p.pay()) + '\n'
		s += str(PayTask) + '\n'
	except Exception, ex:
		s += str(ex) + '\n'
	toast('abc')
	return s


if __name__ == '__main__':
	p = Pay()
	print p.getOrderInfo('test good', 'test good info', '0.01')