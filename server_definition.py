class server_definition:
	def __init__(self, xmlFile):
		self.symbols = {}

		self.name = None
		self.directory = None
		self.autostart = None
		self.executable = None
		self.args = []
		self.stdout = None
		self.stderr = None

		self.readDefinition(xmlFile, True)

	def isValid(self):
		no_name = not self.name
		no_directory = not self.directory
		no_executable = not self.executable
		no_io = (not self.stdout) or (not self.stderr)
		return not (no_name or no_directory or no_executable or no_io)

	def readDefinition(self, xmlFile, isRoot):
		tree = ElementTree.parse(xmlFile)

		newPath = os.path.dirname(xmlFile)

		savedPath = os.getcwd()
		if newPath != '':
			os.chdir(newPath)

		for defImport in tree.findall('import'):
			self.readDefinition(defImport.text, False)

		for defProperty in tree.findall('property'):
			self.setProperty(defProperty)

		if isRoot:
			nameOb = tree.find('name')
			if nameOb != None:
				self.name = self.replaceSymbols(nameOb.text)

			directoryOb = tree.find('directory')
			if directoryOb != None:
				self.directory = self.replaceSymbols(directoryOb.text)

			autostartOb = tree.find('autostart')
			if autostartOb != None:
				self.autostart = (autostartOb.text == "True")

			executableOb = tree.find('executable')
			if executableOb != None:
				self.executable = self.replaceSymbols(executableOb.text)

			argumentsOb = tree.find('arguments')
			if argumentsOb != None:
				for arg in argumentsOb.findall('arg'):
					self.args.append(self.replaceSymbols(arg.text))

			stdoutOb = tree.find('stdout')
			if stdoutOb != None:
				self.stdout = self.replaceSymbols(stdoutOb.text)

			stderrOb = tree.find('stderr')
			if stderrOb != None:
				self.stderr = self.replaceSymbols(stderrOb.text)
		
		os.chdir(savedPath)

	def setProperty(self, propertyElement):
		key = propertyElement.find('key').text
		value = propertyElement.find('value').text

		value = self.replaceSymbols(value)

		self.symbols[key] = value

	def replaceSymbols(self, string):
		for symbolName in self.symbols.keys():
			string = string.replace('!' + symbolName + '!', self.symbols[symbolName])
		return string

	def __str__(self):
		return str([self.name, self.directory, self.args, self.stdout, self.stderr])
