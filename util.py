class queue:
	items = []
	def pop(self):
		if len(self.items) > 0:
			return self.items.pop(0)
		else:
			return None
		
	def push(self, datum):
		self.items.append(datum)
