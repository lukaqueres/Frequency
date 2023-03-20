class Model:
	def __init__(self, table: str):
		self.table = table

	@staticmethod
	def define_from_dict(name):  # TODO: Finish generation
		def __init__(self, **kwargs):
			Model.__init__(self, name[:-len("Class")])
		newclass = type(name, (Model,), {"__init__": __init__})
		return newclass
