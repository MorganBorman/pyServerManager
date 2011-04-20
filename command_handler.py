from server import server

class command_handler:
	def __init__(self, serverManager, messageQueue):
		self.serverManager = serverManager

		self.messageQueue = messageQueue

		self.goingDown = False

		self.commands = {}
		self.commands_help = {}

		self.commands["start"] = self.start_server
		self.commands["stop"] = self.stop_server
		self.commands["restart"] = self.restart_server
		self.commands["shutdown"] = self.shutdown
		self.commands["available"] = self.list_available
		self.commands["running"] = self.list_running
		self.commands["help"] = self.help

	def command(self, cmdTree):
		rawCmd = cmdTree.text.split(' ')
		id = cmdTree.get('id', '-1')
		cmd = rawCmd[0]
		args = rawCmd[1:]
		status = "Unknown Failure."
		try:
			if cmd in self.commands.keys():
				status = self.commands[cmd](args)
			else:
				status = "Unknown command:'" + cmd + "'"
		except Exception, err:
			return "<xml><response id='" + str(id) + "'>" + repr(err) + "</response></xml>"
		else:
			return "<xml><response id='" + str(id) + "'>" + status + "</response></xml>"
	
	def start_server(self, *args):
		args = args[0]
		name = args[0]
		if name in self.serverManager.server_data.keys():
			if not (name in self.serverManager.servers.keys()):
				self.serverManager.servers[name] = server(self.serverManager.server_data[name], self.messageQueue)
				self.serverManager.servers[name].start()
			elif not self.serverManager.servers[name].is_alive():
				self.serverManager.servers[name] = server(self.serverManager.server_data[name], self.messageQueue)
				self.serverManager.servers[name].start()
			else:
				return name + " is already running."
		else:
			return name + " is not a valid server name."
		return "success"

	def stop_server(self, *args):
		args = args[0]
		name = args[0]
		if name in serverManager.server_data.keys():
			if name in self.serverManager.servers.keys():
				self.serverManager.servers[name].stop()
				del self.serverManager.servers[name]
			else:
				return name + " is not running."
		else:
			return name + " is not a valid server name."
		return "success"

	def restart_server(self, *args):
		args = args[0]
		name = args[0]
		self.serverManager.server_data.keys()
		if name in self.serverManager.server_data.keys():
			if name in self.serverManager.servers.keys():
				self.serverManager.servers[name].restart()
			else:
				return name + " is not running."
		else:
			return name + " is not a valid server name."
		return "success"

	def shutdown(self, *args):
		args = args[0]
		self.serverManager.alive = False
		return "success"

	def list_available(self, *args):
		args = args[0]
		return " ".join(self.serverManager.server_data.keys())

	def list_running(self, *args):
		args = args[0]
		return " ".join(self.serverManager.servers.keys())

	def server_info(self, *args):
		args = args[0]
		name = args[0]
		if name in self.serverManager.server_data.keys():
			srv = self.serverManager.server_data[name]
			return "Info for server: " + name + "\nDirectory:" + srv.directory + "\nExecutable:" + srv.executable + "\nAutostart:" + srv.autostart
		else:
			return name + " is not a valid server name."

	def help(self, *args):
		args = args[0]
		if len(args) == 0:
			return "Help: Welcome to pyServerManager (psm) help.\nType \"help commands\" to get a list of the commands\nType \"help command-name\" to get help about a particular command."
		elif len(args) == 1:
			cmd = args[0]
			if cmd in self.commands.keys():
				if cmd in self.commands_help.keys():
					return "Help: " + self.commands_help[cmd]
				else:
					return "Help: Sorry no help was found for the command:'" + cmd + "'"
			else:
				return "Help: Unknown command:'" + cmd + "'"
		else:
			return "Help: You may request about only one topic at a time."
		
