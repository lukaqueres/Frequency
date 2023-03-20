import json
import os
import doctest

from typing import Optional

from Errors import TranslationNotFoundError

try:
	import logging as logging
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s : %(message)s', level=logging.INFO)
except ImportError:
	from Frills import HastyLogging as logging
	logging.warning("logging not detected, using made-hasty version. Install logging for full support")
try:
	import discord.app_commands.translator as translator
except ImportError:
	translator = None

locales_dir = "locals\\"
locales = {}


class Local:
	def __init__(self, name: str, code: str, translation: dict):
		self.name = name
		self.code = code
		self.translation = translation

	def get(self, text: str):
		try:
			return self.translation[text]
		except KeyError as error:
			raise TranslationNotFoundError(error.__str__())
		except Exception as error:
			raise error

	@staticmethod
	def load(directory: str = locales_dir):
		for file in os.listdir(directory):
			if file.endswith(".json"):
				try:
					with open(f"{directory}{file}", 'r') as c:
						local = json.load(c)
				except Exception as error:
					raise error
				else:
					locales.update({local["code"]: Local(local["name"], local["code"], local["compilation"])})

	@staticmethod
	def all():
		return locales


def locale(code: Optional[str]):
	if not code:
		return Local
	if code in list(locales.keys()):
		return locales[code]
	else:
		pass


def interaction():
	pass


if __name__ == "__main__":
	doctest.testfile("localisation_doctests.txt", verbose=True)
