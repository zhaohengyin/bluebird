

def string_to_packets(string, packet_size):
	string_byte = string.encode()
	content_length = len(string_byte)

	has_write_header = False
	all_packets = []
	while len(string_byte) > 0:
		if not has_write_header:
			cursor = min([packet_size, content_length]) - 4
			content_top = string_byte[:cursor]
			string_byte = string_byte[cursor:]
			all_packets.append(content_length.to_bytes(4, byteorder='big') + content_top)
			has_write_header = True
		else:
			cursor = min([packet_size, content_length])
			content_top = string_byte[:cursor]
			string_byte = string_byte[cursor:]
			all_packets.append(content_top)

	return all_packets


class PacketSender:
	def __init__(self):
		return

	def send(self, s, content, send_bufsize=1024):
		length = len(content)
		header = length.to_bytes(4, 'big')
		all_content = header + content
		while len(all_content) > 0:
			slice = min([len(all_content), send_bufsize])
			send_content = all_content[:slice]
			all_content = all_content[slice:]
			s.send(send_content)


class PacketSolver:
	def __init__(self):
		self.waiting_header = True
		self.packet_recv_length = 0
		self.packet_total_length = 0
		self.packet_recv_content = b''
		self.packet_queue = [] # Packets waiting for decoding...

		self.header = b''
		self.received_header_length = 0

	def reset_recv_status(self):
		self.waiting_header = True
		self.packet_recv_length = 0
		self.packet_total_length = 0
		self.packet_recv_content = b''
		self.header = b''
		self.received_header_length = 0

	def get(self):
		if len(self.packet_queue) > 0:
			packet = self.packet_queue[0]
			self.packet_queue = self.packet_queue[1:]
			return packet
		return None

	def parse(self, packet):
		if len(packet) == 0:
			return

		if self.waiting_header:
			if len(packet) < 4 - self.received_header_length:
				# header is not complete.
				self.header += packet
				self.received_header_length += len(packet)
				return
			else:
				# header is complete.
				self.header += packet[:4 - self.received_header_length]
				packet = packet[4 - self.received_header_length:]
				self.received_header_length = 4
				self.packet_total_length = int.from_bytes(self.header, 'big')
				# print("Packet Total Length =", self.packet_total_length)
				self.waiting_header = False

		# Assert: when reaching here, the packet variable does not contain header.

		if len(packet) + self.packet_recv_length >= self.packet_total_length:
			# Contain next packet...
			last_content = packet[:self.packet_total_length - self.packet_recv_length]
			self.packet_recv_content += last_content
			self.packet_queue.append(self.packet_recv_content)
			remain_packet = packet[self.packet_total_length - self.packet_recv_length:]

			# do reset.
			self.reset_recv_status()

			# parse the remaining part.
			self.parse(remain_packet)

		else:
			self.packet_recv_content += packet
			self.packet_recv_length += len(packet)


class PacketFlow:
	'''
		The PacketFlow class is used for debugging and testing.
	'''
	def __init__(self, send_packet_size=1024):
		self.send_packet_size = send_packet_size
		self.buffer = b''
		self.packet_queue = []

	def input_flow(self, packet_flow):
		# print(packet_flow)
		for packet in packet_flow:
			self.buffer += packet
		# self.buffer += sum(packet_flow)
		while len(self.buffer) > self.send_packet_size:
			send_packet = self.buffer[:self.send_packet_size]
			self.buffer = self.buffer[self.send_packet_size:]
			self.packet_queue.append(send_packet)

	def end_flow(self):
		self.packet_queue.append(self.buffer)
		self.buffer = b''
