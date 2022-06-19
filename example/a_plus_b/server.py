from bluebird import FunctionServer
import numpy as np


def add(a, b):
	return a + b


def minus(a, b):
	return a - b


if __name__ == '__main__':
	server = FunctionServer(host='localhost', port=12345)
	server.function_handler.add_func('add', add)
	server.function_handler.add_func('minus', minus)
	server.run()
