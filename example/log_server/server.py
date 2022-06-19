from bluebird import FunctionServer, FunctionHandler


class LoggerFunctionHandler(FunctionHandler):
	def __init__(self):
		super(LoggerFunctionHandler, self).__init__()
		self.logs = []

	def init_class_function(self):
		self.add_class_func('add_log', self.add_log)
		self.add_class_func('get_log', self.get_log)

	def add_log(self, log):
		self.logs.append(log)

	def get_log(self, n=5):
		return self.logs[-n:]


if __name__ == '__main__':
	server = FunctionServer(host = 'localhost', port = 12345)
	server.function_handler = LoggerFunctionHandler()
	server.run()
