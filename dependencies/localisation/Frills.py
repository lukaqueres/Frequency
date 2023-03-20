import doctest


class HastyLogging:
	"""
	It is a placeholder class used for replacing not installed logging


	@note It would most likely be not

	@version 1.0.0
	@author lukaqueres

	Examples:

	>>> HastyLogging.warning("I am a hasty - nasty class!")
	localisation - WARNING : I am a hasty - nasty class!
	>>> HastyLogging.info("I am used in place of that more normal logging module")
	localisation - INFO : I am used in place of that more normal logging module
	>>> HastyLogging.debug("I am for debug purposes only!")
	localisation - DEBUG : I am for debug purposes only!
	"""

	format = "localisation - %(levelname)s : %(message)s"
	"""
	@param format: Format of sent message
	"""
	def __init__(self):
		pass

	@staticmethod
	def debug(message: str):
		"""
		Prints debug
		@param message: Message displayed as the debug message
		@return:
		"""
		print(HastyLogging.format % {"levelname": "DEBUG", "message": message})

	@staticmethod
	def info(message: str):
		"""
		Prints info
		@param message: Message displayed as an info message
		@return:
		"""
		print(HastyLogging.format % {"levelname": "INFO", "message": message})

	@staticmethod
	def warning(message: str):
		"""
		Prints warning
		@param message:  Message displayed as an warning message
		@return:
		"""
		print(HastyLogging.format % {"levelname": "WARNING", "message": message})


if __name__ == "__main__":
	doctest.run_docstring_examples(HastyLogging, globals())
