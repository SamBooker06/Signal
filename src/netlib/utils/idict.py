# Indexable dictionary. Ease of use
class idict(dict):
	def __init__(self, iv={}):
		super().__init__(iv)

		self.__dict__ = self


