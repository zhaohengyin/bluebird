from bluebird.packet_model import PacketSolver, PacketSender
from bluebird.byte_ops import *
import socket


class FunctionHandler:
	def __init__(self):
		self.function_dispatcher = {}
		self.class_function_dispatcher = {}
		self.init_class_function()

	def init_class_function(self):
		return

	def add_class_func(self, name, func):
		if name not in self.function_dispatcher and name not in self.class_function_dispatcher:
			self.class_function_dispatcher[name] = func

	def add_func(self, name, func):
		if name not in self.function_dispatcher and name not in self.class_function_dispatcher:
			self.function_dispatcher[name] = func

	def call_func(self, name, args):
		if name in self.function_dispatcher:
			try:
				result = self.function_dispatcher[name](**args)
				return result

			except Exception:
				return None

		elif name in self.class_function_dispatcher:
			try:
				result = self.class_function_dispatcher[name](**args)
				return result

			except Exception:
				return None

		return None


class FunctionServer:
	def __init__(self, host='localhost', port=12345):
		self.socket = socket.socket()
		self.host = host
		self.port = port

		self.packet_solver = PacketSolver()
		self.packet_sender = PacketSender()

		self.function_handler = FunctionHandler()

	def run(self, recv_bufsize=1024, send_bufsize=1024):
		self.socket.bind((self.host, self.port))
		self.socket.listen()

		while True:
			conn, addr = self.socket.accept()
			print('Connection established:', addr)
			with conn:
				flag = True

				while flag:
					data = conn.recv(recv_bufsize)
					self.packet_solver.parse(data)

					while len(self.packet_solver.packet_queue) > 0:
						packet = self.packet_solver.get()
						request = decode_arg_dict(packet.decode())

						# print(request)
						function_name = request['func']
						function_args = request['args']

						result = self.function_handler.call_func(function_name, function_args)

						# print('Result', result)
						self.packet_sender.send(conn, serialize_object_to_string(result).encode(),
												send_bufsize=send_bufsize)

					flag = len(data) > 0

			conn.close()