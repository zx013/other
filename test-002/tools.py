#-*- coding:utf-8 -*-
import socket
import hashlib
import random
from functools import wraps
from itertools import repeat

def error_func(base=None):
	def run_func(func):
		#@wraps
		def run(*argv, **kwargv):
			try:
				return func(*argv, **kwargv)
			except Exception, ex:
				return base
		return run
	return run_func

def repeat_func(num=None):
	def run_func(func):
		#@wraps
		def run(*argv, **kwargv):
			for i in repeat(0, num + 1 if num > 0 else 1) if isinstance(num, int) else repeat(0):
				ret = func(*argv, **kwargv)
				if ret:
					return ret
			return ret
		return run
	return run_func

def getOutTradeNo():
	key = str(int(time.time() * 1000))
	key += str(random.random())[2:]
	key = key[:20]
	return key

@error_func('127.0.0.1')
def getIp():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = socket.getservbyname('http', 'tcp')
	s.connect(('www.baidu.com', port))
	ip = s.getsockname()[0]
	s.close()
	return ip

def getMd5(s):
	md = hashlib.md5(s)
	return md.hexdigest()

def getSha1(s):
	sh = hashlib.sha1(s)
	return sh.hexdigest()

def getData(data, func=lambda x: x):
	s = ''
	for key in sorted(data):
		s += '&%s=%s' % (key, func(data[key]))
	s = s[1:]
	return s