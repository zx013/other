#-*- coding:utf-8 -*-
import math
from core.clock import Clock
from core.tools import Iterate, Tools

#����ͼ�ε���ؼ���
class Geometry(object):
	#�Ƕ�ת��Ϊ����
	@staticmethod
	def radian(angle):
		return angle * math.pi / 180

	#����ת��Ϊ�Ƕ�
	@staticmethod
	def angle(radian):
		return radian * 180 / math.pi

	@staticmethod
	def sin(angle):
		return math.sin(Geometry.radian(angle))

	@staticmethod
	def cos(angle):
		return math.cos(Geometry.radian(angle))

	@staticmethod
	def asin(ratio):
		return Geometry.angle(math.asin(ratio))

	@staticmethod
	def acos(ratio):
		return Geometry.angle(math.acos(ratio))

	@staticmethod
	def atan(ratio):
		return Geometry.angle(math.atan(ratio))

	#����ͶӰ����
	@staticmethod
	def shadow(pos1, pos2):
		x1, y1 = pos1
		x2, y2 = pos2
		return abs(x2 - x1), abs(y2 - y1)

	#���û���
	#�����������
	@staticmethod
	def distance(pos1, pos2):
		x1, y1 = pos1
		x2, y2 = pos2
		return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

	#������Բ��������ͬһ�����Ϸ���None
	@staticmethod
	def circle_center(pos1, pos2, pos3):
		x1, y1 = pos1
		x2, y2 = pos2
		x3, y3 = pos3
		if pos1 == pos2 == pos3:
			x = x1
			y = y1
		elif pos1 == pos2 != pos3:
			x = (x1 + x3) / 2
			y = (y1 + y3) / 2
		elif pos1 == pos3 != pos2:
			x = (x1 + x2) / 2
			y = (y1 + y2) / 2
		elif pos2 == pos3 != pos1:
			x = (x1 + x2) / 2
			y = (y1 + y2) / 2
		else:
			a = 2 * (x2 - x1)
			b = 2 * (y2 - y1)
			c = x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1
			d = 2 * (x3 - x2)
			e = 2 * (y3 - y2)
			f = x3 * x3 + y3 * y3 - x2 * x2 - y2 * y2
			g = b * d - e * a
			if g:
				x = (b * f - e * c) / g
				y = (d * c - a * f) / g
			else:
				x = None
				y = None
		return x, y

	#�����߽��㣬ƽ�з���None
	@staticmethod
	def intersect_line(line1, line2):
		x11, y11 = line1.source
		x12, y12 = line1.target
		x21, y21 = line2.source
		x22, y22 = line2.target
		a = x11 - x12
		b = y11 - y12
		c = x11 * y12 - x12 * y11
		d = x21 - x22
		e = y21 - y22
		f = x21 * y22 - x22 * y21
		g = b * d - e * a
		if g:
			x = (a * f - d * c) / g
			y = (b * f - e * c) / g
		else:
			x = None
			y = None
		return x, y

	#�ߺͻ��Ľ���
	@staticmethod
	def intersect_arc(line1, arc2):
		x11, y11 = line1.source
		x12, y12 = line1.target
		x21, y21 = arc2.source
		x22, y22 = arc2.target

	#��ת��������Բ��˳ʱ����ת�����Ƕ���Ϊ��ʱ��
	@staticmethod
	def rotate(pos, center, angle):
		if angle == 0:
			return pos
		x, y = pos
		rx, ry = center
		rotate = Geometry.radian(angle) 
		sin = math.sin(rotate)
		cos = math.cos(rotate)
		rotate_x = (y - ry) * sin + (x - rx) * cos + rx
		rotate_y = (y - ry) * cos - (x - rx) * sin + ry
		return rotate_x, rotate_y

	#ƫ�ƣ�pos�ƶ�offset����
	@staticmethod
	def offset(pos, offset):
		x, y = pos
		offset_x, offset_y = offset
		return x + offset_x, y + offset_y
	
	@classmethod
	def test(self):
		print Geometry.rotate((0, 0), (1, 0), -90)
		print Geometry.rotate((0, 0), (1, 0), 90)
		print Geometry.rotate((0, 0), (1, 0), 180)
		print Geometry.rotate((0, 0), (1, 0), 270)
		print Geometry.rotate((0, 0), (1, 0), 360)


#��������һЩ��������ԭ��y��˳ʱ����תrotate���ƶ�pos��õ�
class Coordinate(object):
	def __init__(self, **kwargs):
		rotate = kwargs.get('rotate', 0.0)
		self.set_rotate(rotate)

		offset = kwargs.get('offset', (0.0, 0.0))
		self.set_offset(offset)

		expand = kwargs.get('expand', 0.0)
		self.set_expand(expand)

	#�����������
	def set_rotate(self, rotate):
		self.rotate = rotate

	#λ�ã��������
	def set_offset(self, offset):
		self.offset = offset
		self.offset_x, self.offset_y = self.offset

	#����
	def set_expand(self, expand):
		self.expand = expand

	#���û���
	#����offset, rotate�ƶ���ת��pos��λ��
	def adjust(self, pos):
		pos = Geometry.rotate(pos, (0, 0), self.rotate)
		pos = Geometry.offset(pos, self.offset)
		return pos


#�������Ź켣�˶�
#����������ײ�жϷ������ƶ��ٶȳ���������Բ�뾶��
#ÿ��һ֡���ƶ�һС�ξ��룬�ٶȿ���֡���࣬�ٶ�����֡���٣����ٱ�֤һ��ʱ��Ƭһ֡��
#ÿһ��ʱ��Ƭ��������֡���ݣ�ÿһ֡��������ײ���
#A�����ƶ����γ�A1��A2��A3��֡
#B�����ƶ����γ�B1��B2��֡
#A��B��ײ��ΪA1��A2��A3��B1��B2����ײ
class Motion(object):
	#��֮֡������ƶ�����
	frame_move = 2

	def __init__(self, **kwargs):
		#�ٶȣ�ÿ��ʱ��Ƭ���еľ���
		speed = kwargs.get('speed', 0.0)
		self.speed = Iterate(speed, input=Clock.convert_frequency, output=Clock.convert_frequency)
		
		#���ٶȣ�ÿ��ʱ��Ƭ��ת�ĽǶ�
		self.velocity = kwargs.get('velocity', 0.0)

		#time�����е���ʱ��Ƭ���������˶�
		self.time = kwargs.get('time', 0)

		#ѭ������
		self.cycle = kwargs.get('cycle', 1)

	def move(self):
		t = Tools.count()
		for c in Tools.repeat(self.cycle):
			pos = self.source #ʱ��Ƭ���ʱ��λ��
			residual = self.distance #ʣ�೤��
			while True:
				speed = self.speed(t.next()) #ÿ��ʱ��Ƭ�������ٶ�
				#ÿһ֡�������ڵĵ㣬�����ɸ�
				frame = [pos]
				move = self.frame_move if speed > 0 else -self.frame_move
				for step in xrange(0, int(abs(speed)), move):
					if not step: #��һ��Ϊpos����speedС��1��xrange���Ϊ��
						continue
					if abs(step) > residual: #�ƶ��������ÿ֡�����ĵ㣬ֱ������
						break
					frame.append(self.step(pos, step))
				pos = self.step(pos, speed) #�ƶ�speed����
				frame.append(pos)
				yield frame
				if pos == self.target: #ǡ�õ���Ŀ���
					break
				if abs(speed) > residual: #������ִ��󣬵������һ����ΪĿ��㣬����ʣ�����������
					break
				residual -= speed