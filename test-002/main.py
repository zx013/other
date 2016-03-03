#-*- coding:utf-8 -*-
__version__ = '1.9.0'
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from pay import pay_test



class mainApp(App):
	def build(self):
		s = pay_test()
		label = Label(text=s)
		return label

if __name__ == '__main__':
	mainApp().run()
