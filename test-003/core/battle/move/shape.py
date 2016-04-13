#-*- coding:utf-8 -*-
from geometry import Geometry, Coordinate
from core.test import testmethod

#矩形，以矩形下底边中点为原点
class Rect(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#宽度
		self.width = kwargs['width']

		#高度
		self.height = kwargs['height']

		#包络圆心
		self.wrap_center = (0, self.height / 2)

		#包络半径
		self.wrap_radius = Geometry.distance(self.wrap_center, (self.width / 2, 0))

	@testmethod
	def test(self):
		rect = Rect(offset=(1.0, 1.0), width=2.0, height=4.0)
		print rect.wrap_center, rect.wrap_radius
		rect.set_rotate(45.0)
		print rect.adjust(rect.wrap_center)


#扇形，以圆心为原点
class Sector(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#半径
		self.radius = kwargs['radius']

		#角度
		self.angle = kwargs.get('angle', 90.0)

		#圆心
		self.center = (0, 0)

		x = Geometry.sin(self.angle / 2) * self.radius
		y = Geometry.cos(self.angle / 2) * self.radius

		self.source = x, y
		self.target = -x, y

		#外切圆心，外切半径
		if self.angle < 90: #三点求圆
			self.wrap_center = Geometry.circle_center(self.source, self.target, self.center)
			self.wrap_radius = Geometry.distance(self.wrap_center, self.center)
		elif self.angle < 180: #两侧点中点
			self.wrap_center = (0, y)
			self.wrap_radius = x
		else: #所在的圆
			self.wrap_center = self.center
			self.wrap_radius = self.radius

	@testmethod
	def test(self):
		sector = Sector(radius=2.0, angle=90.0)
		print sector.wrap_center, sector.wrap_radius


#描述物体的形状
class Shape(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#形状组成，由扇形和矩形组成
		self.compose = kwargs.get('compose', [])

	#快速碰撞
	def wrap_collide(self, shape):
		for c1 in self.compose:
			for c2 in shape.compose:
				#先根据扇形和矩形自身的坐标调整
				r1 = self.adjust(c1.adjust(c1.wrap_center)) #用缓存避免重复计算
				r2 = shape.adjust(c2.adjust(c2.wrap_center))
				distance = Geometry.distance(r1, r2)
				if distance < c1.wrap_radius + c2.wrap_radius:
					return True
		return False

	#常规碰撞
	def collide(self, shape):
		if not self.wrap_collide(shape):
			return False
		for c1 in self.compose:
			for c2 in shape.compose:
				pass
		return True

	@classmethod
	def sample(self):
		return Shape(compose=[Rect(width=2.0, height=4.0), Sector(radius=2.0, angle=90.0)])

	@testmethod
	def test(self):
		shape1 = Shape.sample()
		shape2 = Shape(compose=[Rect(width=2.0, height=4.0, offset=(0.0, 5.0)), Sector(radius=2.0, angle=90.0, offset=(0.0, 5.0))])
		print shape1.wrap_collide(shape2)
		shape2.compose[0].set_offset((0.0, 4.0))
		shape2.compose[1].set_offset((0.0, 4.0))
		print shape1.wrap_collide(shape2)