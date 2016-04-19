#-*- coding:utf-8 -*-
from geometry import Geometry, Coordinate, Motion

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
		y += step
		if y > self.length:
			y = self.length
		return x, y

	@classmethod
	def test(self):
		line = Line(length=20.0, speed=500.0, cycle=2)
		g = line.move()
		for p in g:
			print p

#弧
#middle==0.0为圆，middle为0.0时为逆时针，middle为-0.0时为顺时针
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
		if middle:
			self.target = (0, self.length)
		else:
			self.target = self.source

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

		#上一个点
		self.last_step = self.source

	def step(self, pos, step):
		angle = Geometry.angle(step / self.radius)
		middle = self.middle[0]
		if str(middle)[0] != '-': #逆时针
			angle = 360 - angle
		x, y =  Geometry.rotate(pos, self.center, angle)

		last = self.last_step[0] #上一个位置x的值，用来判断圆形的时候是否超出范围
		self.last_step = x, y

		#每次移动不超过半圈
		if middle * x < 0:
			return self.target
		elif middle == 0:
			if str(middle)[0] != '-':
				if last < 0 and x > 0:
					return self.target
			else:
				if last > 0 and x < 0:
					return self.target
		return x, y


	@classmethod
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
		for route in self.compose:
			generator = route.move()
			for frame in generator:
				frame = [self.adjust(route.adjust(pos)) for pos in frame] #根据地图偏移进行调整

				start = frame[0] #起点
				end = frame[-1] #终点
				frame = frame[1:] #包含的帧
				direct = Geometry.atan((end[0] - start[0]) / (end[1] - start[1])) #方向

				step = {'start': start, 'end': end, 'frame': frame, 'direct': direct}
				yield step

	@classmethod
	def sample(self):
		return Route(compose=[Line(length=2.0, speed=50.0, cycle=2, rotate=90.0), Arc(offset=(0.0, 20.0), length=20.0, middle=-10.0, speed=1500.0)])

	@classmethod
	def test(self):
		route = Route.sample()
		g = route.move()
		for p in g:
			print p