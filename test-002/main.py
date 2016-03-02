#-*- coding:utf-8 -*-
__version__ = '1.9.0'
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from pay import test, pay
from toast import toast


class mainApp(App):
	def build(self):
		test()
		s = pay()
		label = Label(text=s)
		toast('abc')
		return label

if __name__ == '__main__':
	mainApp().run()
