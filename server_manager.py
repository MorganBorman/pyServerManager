from util import queue
from command_handler import command_handler
from control_intersponder import control_intersponder
from server_definition import server_definition

from os.path import join
import threading, glob, time, os

class server_manager(threading.Thread):
	def __init__(self, xml_files_path, uds_file_path):
		threading.Thread.__init__(self)
		self.xml_files_path = xml_files_path

		self.messageQueue = queue()

		self.server_data = {}
		self.servers = {}
		self.autostart_server_names = []

		self.read_server_xml_files()

		self.commandHandler = command_handler(self, self.messageQueue)
		self.controlIntersponder = control_intersponder(self.commandHandler, uds_file_path)
		self.controlIntersponder.start()

		self.alive = True

	def read_server_xml_files(self):
		self.server_data = {}		
		self.autostart_server_names = []

		for path in glob.glob(join(self.xml_files_path + '/*')):
			name = os.path.basename(path).split('.')[0]
			definition = server_definition(path)

			if definition.isValid():
				self.server_data[name] = definition

				if definition.autostart:
					self.autostart_server_names.append(name)


	def run(self):
		cnt = 10
		while self.alive:
			if cnt >= 10:
				self.read_server_xml_files()
				cnt = 0
			else:
				cnt += 1
			

			message_data = 1
			while message_data != None:
				message_data = self.messageQueue.pop()
				if message_data:
					print message_data
			time.sleep(1)

		print "Main flow exit"
		self.controlIntersponder.exit()
		for key in self.servers.keys():
			try:
				self.servers[key].stop()
				print "killed", key, "in preparation for exit."
			except:
				print "failed to kill", key

	def autostart_all(self):
		for server_name in self.autostart_server_names:
			self.commandHandler.start_server(server_name)

	def start_list(self, name_list):
		for server_name in name_list:
			self.commandHandler.start_server(server_name)
