from bluebird import call_remote_func
import numpy as np


if __name__ == '__main__':
	result = call_remote_func(host = 'localhost', port = 12345,
							  func = 'add', args = {'a': np.array([1., 2.]), 'b': np.array([3., 4.])})
	
	print(result)

