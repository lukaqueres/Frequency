from typing import Optional


class PsycopgSuiteError(Exception):
	def __init__(self, message: Optional[str] = None, query: Optional[str] = None, *args):
		self.message = message
		self.query = query
		super(PsycopgSuiteError, self).__init__(message, *args)


class PsycopgSuiteValueError(PsycopgSuiteError):
	def __init__(self, message: Optional[str] = None, value: Optional[str] = None, *args):
		self.message = message
		self.value = value
		super(PsycopgSuiteError, self).__init__(message, *args)
