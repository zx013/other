#-*- coding:utf-8 -*-
import jnius_config
jnius_config.add_classpath('.', 'alipaySdk-20160120.jar', 'paydemoactivity.jar', 'libammsdk.jar')
from jnius import autoclass, cast
from toast import toast

PythonActivity = autoclass('org.renpy.android.PythonActivity')
context = cast('android.app.Activity', PythonActivity.mActivity)

'''
PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
Class = autoclass('java.lang.Class')
Bundle = autoclass('android.os.Bundle')
String = autoclass('java.lang.String')

current = cast('android.app.Activity', PythonActivity.mActivity)

#AndroidManifest.xml
#<uses-permission android:name='android.permission.INTERNET' />
#<activity android:name='com.alipay.sdk.pay.demo.H5PayDemoActivity' />
#modify: .buildozer/android/platform/python-for-android/dist/myapp/templates/AndroidManifest.tmpl.xml
#delete: setContentView(R.layout.pay_main);
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


from kivy.clock import Clock

import time
import random
import urllib
#import functools

String = autoclass('java.lang.String')
#URLEncoder = autoclass('java.net.URLEncoder')

PayTask = autoclass('com.alipay.sdk.app.PayTask')
SignUtils = autoclass('com.alipay.sdk.pay.demo.SignUtils')


class AliPay:
	PARTNER = ''
	SELLER = ''
	RSA_PRIVATE = ''
	RSA_PUBLIC = ''

	def run(self, payInfo):
		alipay = PayTask(context)
		result = alipay.pay(payInfo, True)

		try:
			result = dict([v.split('=') for v in result.replace('{', '').replace('}', '').split(';')])
		except:
			result = {}
		resultStatus = result.get('resultStatus')

		if resultStatus == '9000':
			toast('支付成功')
		elif resultStatus == '8000':
			toast('支付结果确认中')
		else:
			toast('支付失败')
		return result

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

		#thread.start_new_thread(self.run, (payInfo,))
		#Clock.create_trigger(functools.partial(self.run, payInfo))()

		result = self.run(payInfo)
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


import urllib2
import json

WXAPIFactory = autoclass('com.tencent.mm.sdk.openapi.WXAPIFactory')
PayReq = autoclass('com.tencent.mm.sdk.modelpay.PayReq')

class WxPay:
	APP_ID = 'wxd930ea5d5a258f4f'
	url = 'http://wxpay.weixin.qq.com/pub_v2/app/app_pay.php?plat=android'

	def getUrl(self, url):
		request = urllib2.Request(url)
		data = urllib2.urlopen(request)
		result = data.read()
		result = json.loads(result)
		return result

	def getInfo(self, info, key):
		return String(info.get(key, ''))

	def getReq(self, info):
		req = PayReq()
		s = ''
		try:
			s += 'x.' + str(req.appId) + '\n'
			req.appId = 'wxd930ea5d5a258f4f'
			s += 'y.' + str(req.appId) + '\n'
		except Exception, ex:
			pass

		try:
			req.appId = self.getInfo(info, 'appid')
			req.partnerId = self.getInfo(info, 'partnerid')
		except Exception, ex:
			s += 'a.' + str(req.appId) + '\n'
		try:
			req.prepayId = self.getInfo(info, 'prepayid')
			req.nonceStr = self.getInfo(info, 'noncestr')
		except Exception, ex:
			s += 'b.' + str(req.prepayId) + '\n'
		try:
			req.timeStamp = self.getInfo(info, 'timestamp')
			req.packageValue = self.getInfo(info, 'package')
		except Exception, ex:
			s += 'c.' + str(req.timeStamp) + '\n'
		try:
			req.sign = self.getInfo(info, 'sign')
			req.extData = String('app data')
		except Exception, ex:
			s += 'd.' + str(req.sign) + '\n'
		return req, s

	def pay(self):
		s = ''
		api = WXAPIFactory.createWXAPI(context, 'wxb4ba3c02aa476ea1')
		info = self.getUrl(self.url)
		try:
			req, sa = self.getReq(info)
			s += sa
		except Exception, ex:
			s += '3.' + str(ex) + '\n'
		try:
			s += str(api.sendReq(req)) + '\n'
		except Exception, ex:
			s += '4.' + str(ex) + '\n'
		return s


def pay_test():
	s = 'none\n'
	try:
		#p = AliPay()
		p = WxPay()
		result = p.pay()
		s += str(result) + '\n'
	except Exception, ex:
		s += str(ex) + '\n'
	return s


if __name__ == '__main__':
	p = AliPay()
	print p.getOrderInfo('test good', 'test good info', '0.01')
	p = WxPay()
	print p.getUrl(p.url)