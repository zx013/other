#-*- coding:utf-8 -*-
import jnius_config
jnius_config.add_classpath('.', 'alipaySdk-20160120.jar', 'paydemoactivity.jar', 'libammsdk.jar')
from jnius import autoclass, cast
from toast import toast
from tools import *

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
	NOTIFY_URL = 'http://notify.msp.hk/notify.htm'
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
		orderInfo += '&out_trade_no="%s"' % getOutTradeNo()
		orderInfo += '&subject="%s"' % subject
		orderInfo += '&body="%s"' % body
		orderInfo += '&total_fee="%s"' % price
		orderInfo += '&notify_url="%s"' % self.NOTIFY_URL
		orderInfo += '&service="mobile.securitypay.pay"'
		orderInfo += '&payment_type="1"'
		orderInfo += '&_input_charset="utf-8"'
		orderInfo += '&it_b_pay="30m"'
		#orderInfo += '&extern_token="%s"' % extern_token
		orderInfo += '&return_url="m.alipay.com"'
		#orderInfo += '&paymethod="expressGateway"'
		return orderInfo

	def sign(self, content):
		return SignUtils.sign(content, self.RSA_PRIVATE)

	def getSignType(self):
		return 'sign_type="RSA"'



import urllib
import urllib2
import json


WXAPIFactory = autoclass('com.tencent.mm.sdk.openapi.WXAPIFactory')
PayReq = autoclass('com.tencent.mm.sdk.modelpay.PayReq')

class WxPay:
	NOTIFY_URL = 'http://notify.msp.hk/notify.htm'
	ACCESS_TOKEN = ''
	APP_ID = 'wxb4ba3c02aa476ea1'
	PARTNER_ID = ''
	PARTNER_KEY = ''

	def __init__(self):
		Clock.schedule_interval(self.getAccessToken, 3500)

	@error_func()
	def getUrl(self, url, **kwargs):
		request = urllib2.Request(url=url, **kwargs)
		data = urllib2.urlopen(request)
		result = data.read()
		result = json.loads(result)
		return result

	@repeat_func(3)
	def getAccessToken(self):
		url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=APPSECRET' % self.APP_ID
		result = self.getUrl(url)
		if not result:
			return
		if result.has_key('errcode'):
			return
		self.ACCESS_TOKEN = result['access_token']

	def getPackage(self, body, attach, total_fee):
		package = 'bank_type=WX'
		package += '&body=%s' % body
		package += '&attach=%s' % attach
		package += '&partner=%s' % self.PARTNER_ID
		package += '&out_trade_no=%s' % getOutTradeNo()
		package += '&total_fee=%s' % total_fee
		package += '&fee_type=1'
		package += '&notify_url=%s' % self.NOTIFY_URL
		package += '&spbill_create_ip=%s' % getIp()
		package += '&input_charset="UTF-8"'
		package += '&key=%s' % self.PARTNER_KEY
		return package

	def sign(self, package):
		value = getMd5(package)
		value = value.upper()
		package = urllib.quote(package, safe='=&')
		package += '&sign=%s' % value
		return package

	def getOrder(self):
		url = 'https://api.weixin.qq.com/pay/genprepay?access_token=%s' % self.ACCESS_TOKEN
		result = self.getUrl(url)
		if not result:
			return
		if result.get('errcode') != 0:
			return
		prepayid = result['prepayid']


	def getInfo(self, info, key):
		return String(info.get(key, ''))

	def getReq(self):
		#直接赋值会报错，放在jar里面则不会出错
		wxpay = autoclass('wxapi.WXPay')
		wp = wxpay()
		req = wp.getReq()
		return req

		req = PayReq()
		s = ''
		try:
			s += 'x.' + str(req.appId) + '\n'
			s += 't.%s, %s' % (str(hasattr(req, 'appId')), type(req.appId)) + '\n'
			#req.appId = 'wxd930ea5d5a258f4f'
			setattr(req, 'appId', 'wxd930ea5d5a258f4f')
			s += 'y.' + str(req.appId) + '\n'
		except Exception, ex:
			s += 'z.' + str(req.appId) + '\n'

		try:
			req.appId = self.getInfo(info, 'appid')
			req.partnerId = self.getInfo(info, 'partnerid')
		except Exception, ex:
			s += 'a.' + str(req.appId) + '\n'

		req.prepayId = self.getInfo(info, 'prepayid')
		req.nonceStr = self.getInfo(info, 'noncestr')
		req.timeStamp = self.getInfo(info, 'timestamp')
		req.packageValue = self.getInfo(info, 'package')
		req.sign = self.getInfo(info, 'sign')
		req.extData = String('app data')
		return req, s

	def pay(self):
		s = ''
		api = WXAPIFactory.createWXAPI(context, 'wxb4ba3c02aa476ea1')
		api.registerApp(self.APP_ID)
		#url = 'http://wxpay.weixin.qq.com/pub_v2/app/app_pay.php?plat=android'
		#info = self.getUrl(url)
		req = self.getReq()
		result = api.sendReq(req) #result is True, but wx is not open

		return result


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