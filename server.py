import threading, subprocess, time

class server(threading.Thread):
	def __init__(self, serverDef, messageQueue):
			threading.Thread.__init__(self)

			self.messageQueue = messageQueue

			self.serverDef = serverDef
			self.name = serverDef.name

			self.args = [serverDef.name] + serverDef.args

			self.process = None

			self.stay_online = True

			self.start_time = time.time()

	def run(self):
			serverDef = self.serverDef

			self.stdoutf = open(serverDef.stdout, 'w')
			self.stderrf = open(serverDef.stderr, 'w')
			#subprocess.PIPE
			while self.stay_online:
				self.process = subprocess.Popen(
									self.args, 
									executable=serverDef.executable, 
									shell=False, stdout=self.stdoutf, 
									stderr=self.stderrf, 
									env=os.environ, 
									cwd=serverDef.directory
								)
				self.messageQueue.push("server " + self.name + " spawned with a pid of " + str(self.process.pid))
				return_code = self.process.wait()
				self.process = None
				self.messageQueue.push("server " + self.name + " passed away with a return code of " + str(return_code))
				self.end_time = time.time()
				if (self.end_time - self.start_time) < 15: #we don't want to keep respawning it if it's crashing
					self.stay_online = False
					
	def is_online(self):
		return not (self.process == None)
	
	def stop(self):
		self.stay_online = False
		if self.process != None:
			self.process.kill()

	def restart(self):
		if self.process != None:
			self.process.kill()
