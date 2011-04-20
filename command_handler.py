class command_handler:
	def __init__(self, serverManager, messageQueue):
		self.serverManager = serverManager

		self.messageQueue = messageQueue

		self.goingDown = False

		self.commands = {}

		self.commands["start"] = self.start_server
		self.commands["stop"] = self.stop_server
		self.commands["restart"] = self.restart_server
		self.commands["shutdown"] = self.shutdown

	def command(self, cmdTree):
		rawCmd = cmdTree.text.split(' ')
		id = cmdTree.get('id', '-1')
		cmd = rawCmd[0]
		args = rawCmd[1:]
		print ">" + cmd + "<>" + str(args) + "<"
		status = "Unknown Failure."
		try:
			if cmd in self.commands.keys():
				if len(args) > 0:
					status = self.commands[cmd](args[0])
				else:
					status = self.commands[cmd]()
			else:
				status = "Unknown command:'" + cmd + "'"
		except:
			return "<xml><response id='" + str(id) + "'>" + status + "</response></xml>"
		else:
			return "<xml><response id='" + str(id) + "'>" + status + "</response></xml>"
	
	def start_server(self, name):
		if name in self.serverManager.server_data.keys():
			if not (name in self.serverManager.servers.keys()):
				self.serverManager.servers[name] = fd_server(self.serverManager.server_data[name], self.messageQueue)
				self.serverManager.servers[name].start()
			elif not self.serverManager.servers[name].is_alive():
				self.serverManager.servers[name] = fd_server(self.serverManager.server_data[name], self.messageQueue)
				self.serverManager.servers[name].start()
			else:
				return name + " is already running."
		else:
			return name + " is not a valid server name."
		return "success"

	def stop_server(self, name):
		if name in serverManager.server_data.keys():
			if name in self.serverManager.servers.keys():
				self.serverManager.servers[name].stop()
				del self.serverManager.servers[name]
			else:
				return name + " is not running."
		else:
			return name + " is not a valid server name."
		return "success"

	def restart_server(self, name):
		self.serverManager.server_data.keys()
		if name in self.serverManager.server_data.keys():
			if name in self.serverManager.servers.keys():
				self.serverManager.servers[name].restart()
			else:
				return name + " is not running."
		else:
			return name + " is not a valid server name."
		return "success"

	def shutdown(self, arg):
		self.serverManager.alive = False
		return "success"
