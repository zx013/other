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


import time

class Time:
	@staticmethod
	def clock():
		return int(time.time() * 1000)

	@staticmethod
	def sleep(tm):
		time.sleep(tm / 1000.0)



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


#几何图形的相关计算
class Geometry:
	#计算投影距离
	@staticmethod
	def shadow(pos1, pos2):
		x1, y1 = map(float, pos1)
		x2, y2 = map(float, pos2)
		return abs(x2 - x1), abs(y2 - y1)

	#计算两点距离
	@staticmethod
	def distance(pos1, pos2):
		x1, y1 = map(float, pos1)
		x2, y2 = map(float, pos2)
		return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

	#三点求圆，三点在同一条线上返回None
	@staticmethod
	def circle_center(pos1, pos2, pos3):
		x1, y1 = map(float, pos1)
		x2, y2 = map(float, pos2)
		x3, y3 = map(float, pos3)
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
			if not g:
				return None
			x = (b * f - e * c) / g
			y = (d * c - a * f) / g
		return x, y

	#两条线交点，平行返回None
	@staticmethod
	def intersect_line(line1, line2):
		x11, y11 = map(float, line1.source)
		x12, y12 = map(float, line1.target)
		x21, y21 = map(float, line2.source)
		x22, y22 = map(float, line2.target)
		a = x11 - x12
		b = y11 - y12
		c = x11 * y12 - x12 * y11
		d = x21 - x22
		e = y21 - y22
		f = x21 * y22 - x22 * y21
		g = b * d - e * a
		if not g:
			return None
		x = (a * f - d * c) / g
		y = (b * f - e * c) / g
		return x, y

	#线和弧的交点
	@staticmethod
	def intersect_arc(line1, arc2):
		x11, y11 = map(float, line1.source)
		x12, y12 = map(float, line1.target)
		x21, y21 = map(float, arc2.source)
		x22, y22 = map(float, arc2.target)
	

	def intersect(wire1, wire2):
		pass

#线段
class Line:
	def __init__(self, **kwargs):
		#源点
		self.source = kwargs.get('source', (0, 0))

		#目标点
		self.target = kwargs.get('target', (0, 0))

#弧
class Arc:
	#源点，目标点，中间点
	#源点，目标点，圆心点
	#圆心点，方向，角度，半径
	def __init__(self, **kwargs):
		#源点
		self.source = kwargs.get('source', (0, 0))

		#目标点
		self.target = kwargs.get('target', (0, 0))

		#圆弧的圆心，圆心点，中间点，半径，展开角
		if kwargs.has_key('center'):
			self.center = kwargs['center']
		else:
			#中间点
			self.middle = kwargs.get('middle', (0, 0))
			self.center = Geometry.circle_center(self.source, self.target, self.middle)

		#半径
		self.radius = Geometry.distance(self.source, self.center)

		#角度
		self.angle ＝ 0
		
		#方向
		self.direct = 0


#描述物体的形状
class Shape:
	def __init__(self, **kwargs):
		#形状，圆形circle，矩形rectangle，扇形sector
		self.type = kwargs.get('type', 'circle')

		#半径
		self.radius = kwargs.get('radius', 0)

		#长宽，圆形长宽设置为直径
		if self.type in ('circle', 'sector'):
			self.width = 2 * self.radius
			self.height = 2 * self.radius
		else:
			self.width = kwargs.get('width', 0)
			self.height = kwargs.get('height', 0)

		#位置
		self.pos = kwargs.get('pos', (0, 0))

	#判断两个形状是否碰撞
	def collide(self, shape):
		#圆形和矩形碰撞视为两个矩形的碰撞
		if self.type == 'circle' and shape.type == 'circle':
			distance = Geometry.distance(self.pos, shape.pos)
			if self.radius + shape.radius >= distance:
				return True
			return False
		else:
			x, y = Geometry.shadow(self.pos, shape.pos)
			if self.width + shape.width >= 2 * x and self.height + shape.height >= 2 * y:
				return True
			return False
		return False

	@staticmethod
	def test():
		s1 = Shape(type='circle', radius=2, pos=(0, 3))
		s2 = Shape(type='circle', radius=3, pos=(3, 0))
		s3 = Shape(type='circle', radius=0.9, pos=(3, 3))
		print s1.collide(s2)
		print s1.collide(s3)
		print s2.collide(s3)

		s1 = Shape(type='rectangle', width=4, height=4, pos=(0, 3))
		s2 = Shape(type='rectangle', width=2, height=4, pos=(3, 0))
		s3 = Shape(type='rectangle', width=1.9, height=1.9, pos=(3, 3))
		print s1.collide(s2)
		print s1.collide(s3)
		print s2.collide(s3)


#描述移动的轨迹
class Route:
	def __init__(self, **kwargs):
		#轨迹包含的线段
		self.line = []

		#运行速度
		self.speed = 0

		#运行时间
		self.time = 0

		#路径包含的点，从源点到目标点依次排列
		self.point = []

	#获取下一个路径点
	def next(self):
		pass

	@staticmethod
	def test():
		route = Route(line=[Line(source=(0, 0), target=(0, 1)), Line(source=(0, 1), target=(1, 1))], speed=1)


class Object(Base):
	def __init__(self):
		#类型，如normal，skill等
		self.type = ''

		#形状，如圆形，矩形，扇形等
		self.shape = Shape()

		#轨迹
		self.route = Route()

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



def main():
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
	Shape.test()
	return o



if __name__ == '__main__':
	main()