#-*- coding:utf-8 -*-
import os
import importlib


def testclass(modulename, cls):
	#Ŀǰ���ظ�ʵ���������µ�����
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


#�Զ�����
#��������sample�Ƿ񷵻���
#���ò���test����
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
				if key[:2] == key[-2:] == '__': #ħ������
					continue
				if not isinstance(cls, type): #�ࣨ����Ϊobject��
					continue
				if module.__name__ != cls.__module__: #�����ģ��
					continue
				if 0 not in [cls.__module__.find(s) for s in allow] and 0 in [cls.__module__.find(s) for s in ignore]:
					continue
				#print key, cls, type(cls)
				testclass(modulename, cls)