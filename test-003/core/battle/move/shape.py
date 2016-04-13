#-*- coding:utf-8 -*-
from geometry import Geometry, Coordinate
from core.test import testmethod

#���Σ��Ծ����µױ��е�Ϊԭ��
class Rect(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#���
		self.width = kwargs['width']

		#�߶�
		self.height = kwargs['height']

		#����Բ��
		self.wrap_center = (0, self.height / 2)

		#����뾶
		self.wrap_radius = Geometry.distance(self.wrap_center, (self.width / 2, 0))

	@testmethod
	def test(self):
		rect = Rect(offset=(1.0, 1.0), width=2.0, height=4.0)
		print rect.wrap_center, rect.wrap_radius
		rect.set_rotate(45.0)
		print rect.adjust(rect.wrap_center)


#���Σ���Բ��Ϊԭ��
class Sector(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#�뾶
		self.radius = kwargs['radius']

		#�Ƕ�
		self.angle = kwargs.get('angle', 90.0)

		#Բ��
		self.center = (0, 0)

		x = Geometry.sin(self.angle / 2) * self.radius
		y = Geometry.cos(self.angle / 2) * self.radius

		self.source = x, y
		self.target = -x, y

		#����Բ�ģ����а뾶
		if self.angle < 90: #������Բ
			self.wrap_center = Geometry.circle_center(self.source, self.target, self.center)
			self.wrap_radius = Geometry.distance(self.wrap_center, self.center)
		elif self.angle < 180: #������е�
			self.wrap_center = (0, y)
			self.wrap_radius = x
		else: #���ڵ�Բ
			self.wrap_center = self.center
			self.wrap_radius = self.radius

	@testmethod
	def test(self):
		sector = Sector(radius=2.0, angle=90.0)
		print sector.wrap_center, sector.wrap_radius


#�����������״
class Shape(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#��״��ɣ������κ;������
		self.compose = kwargs.get('compose', [])

	#������ײ
	def wrap_collide(self, shape):
		for c1 in self.compose:
			for c2 in shape.compose:
				#�ȸ������κ;���������������
				r1 = self.adjust(c1.adjust(c1.wrap_center)) #�û�������ظ�����
				r2 = shape.adjust(c2.adjust(c2.wrap_center))
				distance = Geometry.distance(r1, r2)
				if distance < c1.wrap_radius + c2.wrap_radius:
					return True
		return False

	#������ײ
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