#-*- coding:utf-8 -*-
__version__ = '1.9.0'
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from alipay import Alipay

class mainApp(App):
	def build(self):
		alipay = Alipay()
		s = alipay.run()
		label = Label(text=s)
		return label

if __name__ == '__main__':
	mainApp().run()
