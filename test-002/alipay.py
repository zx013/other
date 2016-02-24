#-*- coding:utf-8 -*-
import string, random
import thread

import jnius_config
jnius_config.add_classpath('.', 'alipaySdk-20160120.jar')
from jnius import autoclass


URLEncoder = autoclass('java.net.URLEncoder')

PayTask = autoclass('com.alipay.sdk.app.PayTask')
#PackageInfo = autoclass('android.content.pm.PackageInfo')
#PackageManager = autoclass('android.content.pm.PackageManager')
#View = autoclass('android.view.View')
#Handler = autoclass('android.os.Handler')
#Message = autoclass('android.os.Message')
#FragmentActivity = autoclass('android.support.v4.app.FragmentActivity')
Toast = autoclass('android.widget.Toast')

class Alipay:
	#商户PID
	PARTNER = ""
	#商户收款账号
	SELLER = ""
	#商户私钥，pkcs8格式
	RSA_PRIVATE = ""
	#支付宝公钥
	RSA_PUBLIC = ""
	SDK_PAY_FLAG = 1
	SDK_CHECK_FLAG = 2

	def getOutTradeNo(self):
		s = list(string.ascii_letters)
		random.shuffle(s)
		return ''.join(s[:14])

	def getOrderInfo(self, subject, body, price):
		orderInfo = "partner=" + "\"" + self.PARTNER + "\""
		orderInfo += "&seller_id=" + "\"" + self.SELLER + "\""
		orderInfo += "&out_trade_no=" + "\"" + self.getOutTradeNo() + "\""
		orderInfo += "&subject=" + "\"" + subject + "\""
		orderInfo += "&body=" + "\"" + body + "\""
		orderInfo += "&total_fee=" + "\"" + price + "\""
		orderInfo += "&notify_url=" + "\"" + "http://notify.msp.hk/notify.htm" + "\""
		orderInfo += "&service=\"mobile.securitypay.pay\""
		orderInfo += "&payment_type=\"1\""
		orderInfo += "&_input_charset=\"utf-8\""
		orderInfo += "&it_b_pay=\"30m\""
		orderInfo += "&return_url=\"m.alipay.com\""
		
		return orderInfo

	def pay(self):
		try:
			payInfo = getOrderInfo("test", "testbody")
			sign = payInfo
			#sign = SignatureUtils.Sign(payInfo, self.RSA_PRIVATE)
			sign = URLEncoder.Encode(sign, "utf-8")
			payInfo += "&sign=\"" + sign + "\"&" + "sign_type=\"RSA\""
			alipay = PayTask(self)
			result = alipay.pay(payInfo, False)

		except Exception, ex:
			Toast.makeText(self, "支付成功", Toast.LENGTH_SHORT).show()

	def run(self):
		#thread.start_new_thread(self.pay, ())
		try:
			Toast.makeText(self, "支付成功", Toast.LENGTH_SHORT).show()
			s = 'success'
		except Exception, ex:
			s = 'failure: ' + str(ex)
		Stack = autoclass('java.util.Stack')
		stack = Stack()
		stack.push('hello')
		stack.push('world')
		return stack.pop() + '\n' + s