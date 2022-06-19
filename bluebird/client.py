from bluebird.packet_model import PacketSolver, PacketSender
from bluebird.byte_ops import *
import socket
import numpy as np


def call_remote_func(host, port, func, args, send_bufsize=1024):
	s = socket.socket()
	sender = PacketSender()
	solver = PacketSolver()

	s.connect((host, port))
	sender.send(s, encode_arg_dict({"func": func, "args": args}).encode())

	flag = True
	result = None
	while flag:
		data = s.recv(send_bufsize)
		solver.parse(data)

		if len(solver.packet_queue) > 0:
			packet = solver.get()
			result = deserialize_string_to_object(packet.decode())
			break

		flag = len(data) > 0

	s.close()
	return result
