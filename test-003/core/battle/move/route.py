#-*- coding:utf-8 -*-
from geometry import Geometry, Coordinate, Motion

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

#��
#middle==0.0ΪԲ��middleΪ0.0ʱΪ��ʱ�룬middleΪ-0.0ʱΪ˳ʱ��
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
		if middle:
			self.target = (0, self.length)
		else:
			self.target = self.source

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

		#��һ����
		self.last_step = self.source

	def step(self, pos, step):
		angle = Geometry.angle(step / self.radius)
		middle = self.middle[0]
		if str(middle)[0] != '-': #��ʱ��
			angle = 360 - angle
		x, y =  Geometry.rotate(pos, self.center, angle)

		last = self.last_step[0] #��һ��λ��x��ֵ�������ж�Բ�ε�ʱ���Ƿ񳬳���Χ
		self.last_step = x, y

		#ÿ���ƶ���������Ȧ
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


#�����ƶ��Ĺ켣
#Coordinate��ƫ��Ϊ��ͼ�ϵ�ƫ��
class Route(Coordinate):
	def __init__(self, **kwargs):
		Coordinate.__init__(self, **kwargs)

		#��ʼ����
		self.toward = kwargs.get('toward', self.rotate)

		#�켣�������߶�
		self.compose = kwargs['compose']

		#���ٶȣ�ÿ��ʱ��Ƭ��ת�ĽǶ�
		self.velocity = kwargs.get('velocity', 20.0)

		#ʣ��Ƕ�
		self.residual = 0.0

	#��ת��ʱ�䲻��һ��ʱ��Ƭ���ۼƣ�ֱ����һ��ʱ��Ƭ����ʱ���м�ʱ
	#�ڹ켣���ƶ�ʱ�������ʱ�仯
	def turn(self, rotate):
		angle = Geometry.standard(rotate - self.toward)
		if not angle:
			return
		direct = self.velocity if angle > 0 else -self.velocity #˳ʱ�����ʱ��Ĳ���
		self.residual += abs(angle) #��Ҫ��ת���ܳ���

		start = self.toward
		while self.residual >= self.velocity: #��������תһ��ʱ��Ƭ
			end = start + direct
			if (end - rotate) * direct > 0:
				end = rotate
			yield {'type': 'rotate', 'start': start, 'end': end}
			self.residual -= self.velocity
			start = end
		self.toward = rotate

	#��ȡ��һ��·���㼰���ڵĹ켣
	def move(self):
		for route in self.compose:
			for frame in route.move():
				frame = [self.adjust(route.adjust(pos)) for pos in frame] #���ݵ�ͼƫ�ƽ��е���

				start = frame[0] #���
				end = frame[-1] #�յ�
				frame = frame[1:] #������֡

				rotate = Geometry.atan((end[0] - start[0]) / (end[1] - start[1])) #���򣬿�������

				if self.velocity: #���ٶ�Ϊ0����ת
					for rotate_frame in self.turn(rotate):
						yield rotate_frame

				yield {'type': 'move', 'start': start, 'end': end, 'frame': frame}

	@classmethod
	def sample(self):
		return Route(compose=[Line(length=2.0, speed=50.0, cycle=2, rotate=90.0), Arc(offset=(0.0, 20.0), length=20.0, middle=-10.0, speed=1500.0)], toward=30.0)

	@classmethod
	def test(self):
		route = Route.sample()
		g = route.move()
		for p in g:
			print p