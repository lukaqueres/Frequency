class Identification:
	connect_url = "postgresql://postgres:postgres@localhost/postgres"
	dbname = "postgres"
	user = "postgres"
	password = "postgres"
	host = "localhost"
	port = 5432

	@staticmethod
	def url(url: str):
		Identification.url = url

	@staticmethod
	def credentials(dbname: str, user: str, password: str, host: str, port: int):
		Identification.dbname = dbname
		Identification.user = user
		Identification.password = password
		Identification.host = host
		Identification.port = port
