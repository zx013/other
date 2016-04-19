#-*- coding:utf-8 -*-
import math
from core.clock import Clock
from core.tools import Iterate, Tools

#几何图形的相关计算
class Geometry(object):
	#角度转换为弧度
	@staticmethod
	def radian(angle):
		return angle * math.pi / 180

	#弧度转换为角度
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

	#计算投影距离
	@staticmethod
	def shadow(pos1, pos2):
		x1, y1 = pos1
		x2, y2 = pos2
		return abs(x2 - x1), abs(y2 - y1)

	#可用缓存
	#计算两点距离
	@staticmethod
	def distance(pos1, pos2):
		x1, y1 = pos1
		x2, y2 = pos2
		return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

	#三点求圆，三点在同一条线上返回None
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

	#两条线交点，平行返回None
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

	#线和弧的交点
	@staticmethod
	def intersect_arc(line1, arc2):
		x11, y11 = line1.source
		x12, y12 = line1.target
		x21, y21 = arc2.source
		x22, y22 = arc2.target

	#旋转，点沿着圆心顺时针旋转，负角度则为逆时针
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

	#偏移，pos移动offset距离
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


#相对坐标的一些操作，绕原点y轴顺时针旋转rotate，移动pos后得到
class Coordinate(object):
	def __init__(self, **kwargs):
		rotate = kwargs.get('rotate', 0.0)
		self.set_rotate(rotate)

		offset = kwargs.get('offset', (0.0, 0.0))
		self.set_offset(offset)

		expand = kwargs.get('expand', 0.0)
		self.set_expand(expand)

	#方向，相对坐标
	def set_rotate(self, rotate):
		self.rotate = rotate

	#位置，相对坐标
	def set_offset(self, offset):
		self.offset = offset
		self.offset_x, self.offset_y = self.offset

	#扩张
	def set_expand(self, expand):
		self.expand = expand

	#可用缓存
	#经过offset, rotate移动旋转后pos的位置
	def adjust(self, pos):
		pos = Geometry.rotate(pos, (0, 0), self.rotate)
		pos = Geometry.offset(pos, self.offset)
		return pos


#物体沿着轨迹运动
#高速物体碰撞判断方法（移动速度超过最大外接圆半径）
#每步一帧，移动一小段距离，速度快则帧数多，速度慢则帧数少（至少保证一个时间片一帧）
#每一个时间片运行若干帧数据，每一帧都进行碰撞检测
#A高速移动，形成A1，A2，A3等帧
#B高速移动，形成B1，B2等帧
#A，B碰撞则为A1，A2，A3与B1，B2的碰撞
class Motion(object):
	#两帧之间最大移动距离
	frame_move = 2

	def __init__(self, **kwargs):
		#速度，每个时间片运行的距离
		speed = kwargs.get('speed', 0.0)
		self.speed = Iterate(speed, input=Clock.convert_frequency, output=Clock.convert_frequency)
		
		#角速度，每个时间片旋转的角度
		self.velocity = kwargs.get('velocity', 0.0)

		#time，运行的总时间片数，匀速运动
		self.time = kwargs.get('time', 0)

		#循环次数
		self.cycle = kwargs.get('cycle', 1)

	def move(self):
		t = Tools.count()
		for c in Tools.repeat(self.cycle):
			pos = self.source #时间片起点时的位置
			residual = self.distance #剩余长度
			while True:
				speed = self.speed(t.next()) #每个时间片的运行速度
				#每一帧物体所在的点，可正可负
				frame = [pos]
				move = self.frame_move if speed > 0 else -self.frame_move
				for step in xrange(0, int(abs(speed)), move):
					if not step: #第一个为pos，若speed小于1，xrange结果为空
						continue
					if abs(step) > residual: #移动距离大于每帧步长的点，直接跳出
						break
					frame.append(self.step(pos, step))
				pos = self.step(pos, speed) #移动speed距离
				frame.append(pos)
				yield frame
				if pos == self.target: #恰好到达目标点
					break
				if abs(speed) > residual: #如果出现错误，导致最后一步不为目标点，则用剩余距离来限制
					break
				residual -= speed