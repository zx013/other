#-*- coding:utf-8 -*-
import os
import importlib

class CLASSOBJ:
	pass

classobj = [type(CLASSOBJ), type(type)]


def testclass(modulename, cls):
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
#ignore�÷ָ�'\\'��β�Ļ�����ǰĿ¼������
def autotest(ignore=[]):
	path = os.curdir + os.sep
	generator = os.walk(path)
	for root, dirs, files in generator:
		root = root.split(path, 1)[1]
		if 0 in [root.find(i) for i in ignore]:
			continue
		for filespath in files:
			if filespath[-3:] != '.py':
				continue
			modulename = os.path.join(root, filespath)[:-3].replace(os.sep, '.')
			module = importlib.import_module(modulename)
			for key, cls in vars(module).items():
				if key[:2] == key[-2:] == '__':
					continue
				if type(cls) not in classobj:
					continue
				testclass(modulename, cls)