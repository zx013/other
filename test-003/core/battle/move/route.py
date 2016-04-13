#-*- coding:utf-8 -*-
from geometry import Geometry, Coordinate, Motion
from core.test import testmethod

#�߶�
class Line(Coordinate, Motion):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)
		Motion.__init__(self, **kwargs)

		#����
		self.length = kwargs['length']

		#Դ��
		self.source = (0, 0)

		#Ŀ���
		self.target = (0, self.length)

		#����
		self.distance = self.length

	#�������ƶ������������ƶ����λ��
	def step(self, pos, step):
		x, y = pos
		return x, y + step

	@testmethod
	def test(self):
		line = Line(length=20.0, speed=500.0, cycle=2)
		g = line.move()
		for p in g:
			print p

#��
class Arc(Coordinate, Motion):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)
		Motion.__init__(self, **kwargs)

		#����
		self.length = kwargs['length']

		middle = kwargs['middle']
		#�м�㣬middle=0ΪԲ
		self.middle = (middle, self.length / 2)

		#Դ��
		self.source = (0, 0)

		#Ŀ���
		self.target = (0, self.length)

		#Բ����Բ��
		if middle:
			self.center = Geometry.circle_center(self.source, self.target, self.middle)
		else:
			self.center = self.middle

		#�뾶
		self.radius = Geometry.distance(self.source, self.center)

		#�Ƕ�
		center_x, center_y = self.center

		if middle > 0:
			self.angle = 360 - 2 * Geometry.acos(center_x / self.radius)
		elif middle < 0:
			self.angle = 2 * Geometry.acos(center_x / self.radius)
		else:
			self.angle = 360

		#����
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


#�����ƶ��Ĺ켣
#Coordinate��ƫ��Ϊ��ͼ�ϵ�ƫ��
class Route(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#�켣�������߶�
		self.compose = kwargs['compose']

	#��ȡ��һ��·���㼰���ڵĹ켣
	def move(self):
		for w in self.compose:
			g = w.move()
			for p in g:
				p = [self.adjust(w.adjust(v)) for v in p] #��������ƫ�ƽ��е���
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