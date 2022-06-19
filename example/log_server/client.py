from bluebird import call_remote_func
import time


if __name__ == '__main__':
	call_remote_func(host='localhost', port=12345, func='add_log', args={'log': 'hello'})
	call_remote_func(host='localhost', port=12345, func='add_log', args={'log': 'it\'s me'})

	time.sleep(5)
	logs = call_remote_func(host='localhost', port=12345, func='get_log', args={'n': 100})

	print(logs)