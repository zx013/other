#-*- coding:utf-8 -*-
import os
import importlib


def testclass(modulename, cls):
	#目前有重复实例创建导致的问题
	if hasattr(cls, 'sample'):
		assert(hasattr(cls.sample, '__call__'))
		assert(isinstance(cls.sample(), cls))

	if hasattr(cls, 'test'):
		print '<{modulename}> {cls} - INIT'.format(modulename=modulename, cls=cls.__name__)
		
		assert(hasattr(cls.test, '__call__'))
		cls.test()
		
		print '<{modulename}> {cls} - DESTROY'.format(modulename=modulename, cls=cls.__name__)
		print
		print


#自动测试
#测试类中sample是否返回类
#调用测试test函数
def autotest(allow=[], ignore=[]):
	path = os.curdir + os.sep
	generator = os.walk(path)
	for root, dirs, files in generator:
		root = root.split(path, 1)[1]
		for filespath in files:
			if filespath[-3:] != '.py':
				continue
			modulename = os.path.join(root, filespath)[:-3].replace(os.sep, '.')
			try:
				module = importlib.import_module(modulename)
			except Exception, ex:
				print 'import library error:', ex
				continue
			for key, cls in vars(module).items():
				if key[:2] == key[-2:] == '__': #魔术方法
					continue
				if not isinstance(cls, type): #类（根类为object）
					continue
				if module.__name__ != cls.__module__: #导入的模块
					continue
				if 0 not in [cls.__module__.find(s) for s in allow] and 0 in [cls.__module__.find(s) for s in ignore]:
					continue
				#print key, cls, type(cls)
				testclass(modulename, cls)