import discord, traceback, sys, os, json
from typing import Optional

from discord import app_commands
from discord.ext import commands

#from packets.discord import PIBot 
	
class File:
	def __init__(self):
		pass;
		#self.file = 'configuration/{}.json'
		
	def write(file, text:str, mode:str = 'a'):
		with open(file, mode) as w:
				w.seek(0, os.SEEK_END); 
				w.write(text);
	
class Configuration:
	def __init__(self):
		self.file = 'configuration/{}.json'
		
	def read(self, category:str, key):
		file = self.file.format(category)
		try:
			with open(file, 'r') as c: # - Open 'configuration.json' file containing work data. Fetch extensions load & log details. -
				configuration = json.load(c); 
		except Exception as error:
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		keys = key.split('.')
		for key in keys
			configuration = configuration[key]
		request = configuration
		return request;
	
class Logger:
	def __init__(self, client, file:str = None):
		self.configuration = client.configuration
		self.time = client.time
		self.logFile = file
		self.file = File();
		self.print = self.configuration.read(category="utilities", key="log.print") 
		self.save = self.configuration.read(category="utilities", key="log.save_to_file")
		self.addTimestamp = self.configuration.read(category="utilities", key="log.add_time_stamp")
		
	def exception(self, text) -> None:
		log = self.configuration.read(category="utilities", key="log.exceptions")
		text = self.time.UTCNow() if self.addTimestamp else '' + ' >>> EXCEPTION: ' + text
		if not log:
			return;
		if log and self.print:
			print(text);
		if log and self.save: 
			self.file.write(file = self.logFile, text = text)
		
	def notify(self, text) -> None:
		log = self.configuration.read(category="utilities", key="log.notices")
		text = self.time.UTCNow() if self.addTimestamp else '' + ' >>> NOTICE: ' + text
		if not log:
			return;
		if log and self.print:
			print(text);
		if log and self.save: 
			self.file.write(file = self.logFile, text = text)
				
	def error(self, text) -> None:
		log = self.configuration.read(category="utilities", key="log.errors")
		text = self.time.UTCNow() if self.addTimestamp else '' + ' >>> ERROR: ' + text
		if not log:
			return;
		if log and self.print:
			print(text);
		if log and self.save: 
			self.file.write(file = self.logFile, text = text)
				
	def debug(self, text) -> None:
		log = self.configuration.read(category="utilities", key="log.debug")
		text = self.time.UTCNow() if self.addTimestamp else '' + ' >>> DEBUG: ' + text
		if not log:
			return;
		if log and self.print:
			print(text);
		if log and self.save: 
			self.file.write(file = self.logFile, text = text)
				
		
