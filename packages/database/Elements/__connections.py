class Connection:
	__url = "postgresql://postgres:postgres@localhost/postgres"

	@staticmethod
	def url(url: str):
		Connection.__url = url
