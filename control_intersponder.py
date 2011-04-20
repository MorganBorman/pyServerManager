from connection_handler import connection_handler

import threading, socket, os

class control_intersponder(threading.Thread):
	def __init__(self, command_handler, uds_file_path):
		threading.Thread.__init__(self)

		self.uds_file_path = uds_file_path

		self.command_handler = command_handler

		self.clients = {}

		self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		try:
		    os.remove(self.uds_file_path)
		except OSError:
		    pass
		self.s.bind(self.uds_file_path)
		self.s.listen(1)

		self.alive = True

	def run(self):
		while self.alive:
			try:
				conn, addr = self.s.accept()
			except socket.error, (value,message):
				if value != 22:
					raise socket.error(value, message)
				else:
					print "Socket accept() failure (Normal on shutdown)"
				self.alive = False
			else:
				self.clients[addr] = connection_handler(self.command_handler, conn, self)
				self.clients[addr].start()
		print "Intersponder shut down."

	def exit(self):
		self.alive = False
		self.s.shutdown(socket.SHUT_RDWR)
		self.s.close()
		try:
		    os.remove(self.uds_file_path)
		except OSError:
		    pass
