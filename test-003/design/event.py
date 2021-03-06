#-*- coding:utf-8 -*-

#主要信号类型
#CLOCK_EVENT, BUFF_EVENT, DEVICE_EVENT

#次要信号类型
#CLOCK_EVENT->时间戳
#BUFF_EVENT -> type -> ['in', 'body', 'out']->['before', 'after']
#DEVICE_EVENT -> type -> key


#ACTION(BUFF) -> EVENT -> BUFF

#CLOCK -> CLOCK_EVENT -> MAIN_BUFF -> BUFF_EVENT -> BUFF

#BUFF只有捕获到了对应的EVENT，才执行相关的动作

#OBJECT
#BUFF
#OBJECT相互作用生成BUFF
#BUFF附属于OBJECT
#BUFF创建或操作OBJECT

#关联OBJECT
#OBJECT和其它OBJECT关联，该OBJECT主动碰撞时影响到关联OBJECT


def testmethod(fun):
	def run(self, *args, **kwargs):
		print '%s: INIT' % self.__name__
		result = fun(self, *args, **kwargs)
		print '%s: DESTROY' % self.__name__
		print
		return result
	run = classmethod(run)
	return run


#封装的函数为递归式与非递归式，递归式由上一次状态计算得出，非递归式则直接算出
#类成员在使用时会随时间片实时改变，其中改变分为内部或外部改变
#不能够被改变的成员无需改动，直接使用即可
#能够被改变的成员必需封装到lambda中，用函数调用形式使用
#外部改变时，递归式只需改变递归值即可，非递归式则需再次封装一层，两者实现的效果不同
class Iterate:
	def __init__(self, func, input=lambda x: x, output=lambda x: x, **kwargs):
		#recurse为递归初值，未设置则视为非递归
		if kwargs.has_key('recurse'):
			self.recurse = kwargs['recurse']

		if hasattr(func, '__call__'):
			self.func = lambda *args, **kwargs: output(func(input(*args, **kwargs)))
		else:
			self.func = lambda *args, **kwargs: output(func)

	def __call__(self, *args, **kwargs):
		if hasattr(self, 'recurse'):
			self.recurse = self.func(self.recurse, *args, **kwargs)
			return self.recurse
		else:
			return self.func(*args, **kwargs)
	
	@testmethod
	def test(self):
		a1 = Iterate(1, recurse=2)
		print a1(), a1(), a1()
		a2 = Iterate(lambda x: x + 1, recurse=2)
		print a2(), a2(), a2()


import time
import itertools

#时间，单位都为毫秒，sleep最小支持1ms，误差1-2%
class Time:
	#间隔，每次运行时间
	interval = 10

	#频率，每秒运行次数
	frequency = 1000 / interval

	@staticmethod
	def clock():
		return int(time.time() * 1000)

	@staticmethod
	def sleep(tm):
		time.sleep(tm / 1000.0)

	@staticmethod
	def through():
		return itertools.count(0)

	#普通时间转换为时间片
	@staticmethod
	def convert_frequency(t):
		return t / Time.frequency


class Event:
	def __init__(self):
		self.event = {}

	#注册事件
	def register(self, e, *args, **kwargs):
		self.event[e] = []

	#生成事件
	def create(self, e, *args, **kwargs):
		for func in self.event[e]:
			if hasattr(func, '__call__'):
				func(*args, **kwargs)

	#绑定事件
	def bind(self, e, *args, **kwargs):
		pass

event = Event()



from functools import wraps

class Base:
	#添加get方法
	def _add_get(self, key, attr):
		def _get(k, v=None):
			return attr.get(k, v)
		_get.func_name = 'get_%s' % key
		setattr(self, _get.func_name, _get)

	#添加set方法
	def _add_set(self, key, attr):
		def _set(k, v):
			attr[k] = v
		_set.func_name = 'set_%s' % key
		setattr(self, _set.func_name, _set)

	#给字典类型添加读写接口
	def wrap_interface(self):
		for key, attr in vars(self).items():
			if not isinstance(attr, dict):
				continue
			self._add_get(key, attr)
			self._add_set(key, attr)

	def _wrap_event(self, func):
		event.register(('FUNCTION_EVENT', func.func_name, 'before'))
		event.register(('FUNCTION_EVENT', func.func_name, 'after'))
		@wraps
		def run(*args, **kwargs):
			event.create(('FUNCTION_EVENT', func.func_name, 'before'), *args, **kwargs)
			result = func(*args, **kwargs)
			result = event.create(('FUNCTION_EVENT', func.func_name, 'after'), result, *args, **kwargs)
			return result
		return run

	#在函数前后绑定事件
	def wrap_event(self):
		for key, attr in vars(self).items():
			if not hasattr(attr, '__call__'):
				continue
			attr = self._wrap_event(attr)



import math

#几何图形的相关计算
class Geometry:
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

	#旋转，点沿着圆心顺时针旋转
	@staticmethod
	def rotate(offset, center, angle):
		x, y = offset
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

#相对坐标的一些操作，绕原点旋转rotate，移动pos后得到
class Coordinate(object):
	def __init__(self, **kwargs):
		rotate = kwargs.get('rotate', 0)
		self.set_rotate(rotate)

		offset = kwargs.get('offset', (0, 0))
		self.set_offset(offset)

		expand = kwargs.get('expand', 0)
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
	#经过pos, rotate移动旋转后pos的位置
	def adjust(self, pos):
		pos = Geometry.rotate(pos, (0, 0), self.rotate)
		pos = Geometry.offset(pos, self.offset)
		return pos


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
		self.angle = kwargs.get('angle', 90)

		#从半径中切除的部分，以实现扇形
		self.slice = kwargs.get('slice', 0)

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
				#先根据自身坐标调整，再根据地图坐标调整
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

	@testmethod
	def test(self):
		shape1 = Shape(compose=[Rect(width=2.0, height=4.0), Sector(radius=2.0, angle=90.0)], offset=(0.0, 0.0), rotate=0.0)
		shape2 = Shape(compose=[Rect(width=2.0, height=4.0), Sector(radius=2.0, angle=90.0)], offset=(0.0, 5.0), rotate=0.0)
		print shape1.wrap_collide(shape2)
		shape2.set_offset((0.0, 4.0))
		print shape1.wrap_collide(shape2)


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
		#speed，每个时间片运行速度
		speed = kwargs.get('speed', 0)
		self.speed = Iterate(speed, input=Time.convert_frequency, output=Time.convert_frequency)

		#time，运行的总时间片数，匀速运动
		self.time = kwargs.get('time', 0)

		#是否周期
		self.cycle = kwargs.get('cycle', 1)

	def move(self):
		t = Time.through()
		for c in xrange(self.cycle):
			slice_pos = self.source #时间片起点时的位置
			residual_distance = self.distance #剩余长度
			while True:
				speed = self.speed(t.next()) #每个时间片的运行速度
				#每一帧物体所在的点，可正可负
				frame_pos = [slice_pos]
				move = self.frame_move if speed > 0 else -self.frame_move
				for step in xrange(0, int(abs(speed)), move):
					if not step: #第一个为slice_pos，若speed小于1，xrange结果为空
						continue
					if abs(step) > residual_distance: #移动距离大于每帧步长的点，直接跳出
						break
					frame_pos.append(self.step(slice_pos, step))
				yield frame_pos
				if abs(speed) > residual_distance:
					break
				slice_pos = self.step(slice_pos, speed) #移动speed距离
				residual_distance -= speed

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
class Route(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#轨迹包含的线段
		self.compose = kwargs['compose']

	#获取下一个路径点
	def move(self):
		for w in self.compose:
			g = w.move()
			for p in g:
				yield p

	@testmethod
	def test(self):
		route = Route(compose=[Line(length=20.0, speed=500.0, cycle=2), Arc(offset=(0.0, 20.0), length=20.0, middle=-10.0, speed=1500.0)])
		g = route.move()
		for p in g:
			print p


class Object(Base):
	def __init__(self):
		#类型，如normal，skill等
		self.type = ''

		#形状，如圆形，矩形，扇形等
		self.shape = Shape()

		#轨迹
		self.route = Route(compose=[])

		#静态属性，不变化或者极少变化的值
		self.attribute = {}

		#动态属性，随时都能变化的值
		self.property = {}

		#包含的buffer，按优先级排列，优先级相同的，按先后顺序
		self.point_buffer = []

		#碰撞其它obj施加的buffer
		self.active_collide_buffer = []

		#被其它obj碰撞施加的buffer
		self.passive_collide_buffer = []

	def create_buffer(self):
		buf = Buffer()
		return buf

	def insert_buffer(self, buf):
		n = 0
		for n, b in enumerate(self.point_buffer):
			if b.priority_level == buf.priority_level and b.create_time > buf.create_time or b.priority_level < buf.priority_level:
				break
		else:
			n += 1
		buf.point_object = self
		self.point_buffer.insert(n, buf)

	def delete_buffer(self, buf):
		self.point_buffer.remove(buf)

	def _active_collide(self, obj):
		for buf in self.active_collide_buffer:
			obj.insert_buffer(buf)

	def _passive_collide(self, obj):
		for buf in self.passive_collide_buffer:
			obj.insert_buffer(buf)

	def active_collide(self, obj):
		self._active_collide(obj)
		obj._passive_collide(self)

	def passive_collide(self, obj):
		self._passive_collide(obj)
		obj._active_collide(self)



class Buffer:
	def __init__(self):
		#属于的object
		self.point_object = None

		#优先级，越大优先级越高
		self.priority_level = 0

		#创建时间
		self.create_time = Time.clock()

	@testmethod
	def test(self):
		o = Object()
		o.wrap_interface()
		o.wrap_event()
		o.set_property('a', 1)
		print o.get_property('a')
		print o.get_attribute('a', 2)

		buf1 = o.create_buffer()
		buf1.priority_level = 0
		o.insert_buffer(buf1)
		Time.sleep(10)
		buf2 = o.create_buffer()
		buf2.priority_level = 3
		o.insert_buffer(buf2)
		Time.sleep(10)
		buf3 = o.create_buffer()
		buf3.priority_level = 3
		o.insert_buffer(buf3)
		Time.sleep(10)
		buf4 = o.create_buffer()
		buf4.priority_level = 0
		o.insert_buffer(buf4)
		o.delete_buffer(buf3)
		print [b.create_time for b in o.point_buffer]



def main():
	Iterate.test()
	Buffer.test()
	Rect.test()
	Sector.test()
	Shape.test()
	Line.test()
	Arc.test()
	Route.test()


if __name__ == '__main__':
	main()