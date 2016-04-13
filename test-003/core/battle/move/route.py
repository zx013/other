#-*- coding:utf-8 -*-
from geometry import Geometry, Coordinate, Motion
from core.test import testmethod

#线段
class Line(Coordinate, Motion):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)
		Motion.__init__(self, **kwargs)

		#长度
		self.length = kwargs['length']

		#源点
		self.source = (0, 0)

		#目标点
		self.target = (0, self.length)

		#距离
		self.distance = self.length

	#输入点和移动步长，返回移动后的位置
	def step(self, pos, step):
		x, y = pos
		return x, y + step

	@testmethod
	def test(self):
		line = Line(length=20.0, speed=500.0, cycle=2)
		g = line.move()
		for p in g:
			print p

#弧
class Arc(Coordinate, Motion):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)
		Motion.__init__(self, **kwargs)

		#长度
		self.length = kwargs['length']

		middle = kwargs['middle']
		#中间点，middle=0为圆
		self.middle = (middle, self.length / 2)

		#源点
		self.source = (0, 0)

		#目标点
		self.target = (0, self.length)

		#圆弧的圆心
		if middle:
			self.center = Geometry.circle_center(self.source, self.target, self.middle)
		else:
			self.center = self.middle

		#半径
		self.radius = Geometry.distance(self.source, self.center)

		#角度
		center_x, center_y = self.center

		if middle > 0:
			self.angle = 360 - 2 * Geometry.acos(center_x / self.radius)
		elif middle < 0:
			self.angle = 2 * Geometry.acos(center_x / self.radius)
		else:
			self.angle = 360

		#距离
		self.distance = Geometry.radian(self.angle) * self.radius

	def step(self, pos, step):
		return Geometry.rotate(pos, self.center, step / self.radius)

	@testmethod
	def test(self):
		arc = Arc(length=20.0, middle=-10.0, speed=1500.0)
		print arc.center, arc.radius, arc.angle, arc.distance
		g = arc.move()
		for p in g:
			print p


#描述移动的轨迹
#Coordinate的偏移为地图上的偏移
class Route(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#轨迹包含的线段
		self.compose = kwargs['compose']

	#获取下一个路径点及所在的轨迹
	def move(self):
		for w in self.compose:
			g = w.move()
			for p in g:
				p = [self.adjust(w.adjust(v)) for v in p] #根据整体偏移进行调整
				yield p

	@classmethod
	def sample(self):
		return Route(compose=[Line(length=20.0, speed=500.0, cycle=2, rotate=90.0), Arc(offset=(0.0, 20.0), length=20.0, middle=-10.0, speed=1500.0)])
	
	@testmethod
	def test(self):
		route = Route.sample()
		g = route.move()
		for p in g:
			print p