import xml.etree.ElementTree as ElementTree
import threading

class connection_handler(threading.Thread):
	def __init__(self, command_handler, connection, controlIntersponder):
		threading.Thread.__init__(self)
		self.controlIntersponder = controlIntersponder
		self.command_handler = command_handler
		self.connection = connection

	def send(self, msg):
		self.connection.send(msg)

	def receive(self):
		return self.connection.recv(4096)

	def run(self):
		while True:
			data = self.receive()
			if not data: break

			try:
			    dataTree = ElementTree.XML(data)
			except:
			    print "Received invalid data:", data
			else:
				for commandTree in dataTree.findall('command'):
					response = self.command_handler.command(commandTree)
					#self.send(ElementTree.tostring(response, encoding="us-ascii")) #for when I return an xmlTree rather than just a string
					self.send(response)
