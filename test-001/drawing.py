#-*- coding:utf-8 -*-
# File name: drawing.py
import kivy
kivy.require('1.7.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import StringProperty

import itertools

class DrawingSpace(GridLayout):
	base_pos = {'right': 1.8, 'top': 1}
	file_list = itertools.cycle([f.decode('utf-8') for f in ['中文001.png', '中文002.png', 'kivy.jpg', 'kivy.jpg']])
	source_1 = StringProperty('')
	source_2 = StringProperty('')

	def __init__(self, **kwargs):
		super(DrawingSpace, self).__init__(**kwargs)
		self.source_1 = self.file_list.next()
		self.source_2 = self.file_list.next()
		Clock.schedule_interval(self.move, 5)
	
	def on_touch_down(self, touch):
		self.move()

	def reset(self, animation, instance):
		self.pos_hint = self.base_pos
		self.source_1 = self.source_2
		self.source_2 = self.file_list.next()
	
	def move(self, *args):
		animation = Animation(pos_hint={'right': self.pos_hint['right'] - self.size_hint[0] / 2, 'top': self.pos_hint['top']}, t='in_out_quad')
		animation.start(self)
		animation.bind(on_complete=self.reset)
		

class DrawingApp(App):
    def build(self):
        return DrawingSpace()

if __name__=="__main__":
    DrawingApp().run()
