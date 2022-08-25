import datetime, os, json
from datetime import datetime, date, timedelta

class Time:
	def __init__(self):
		self.currentUTC = datetime.now(timezone.utc);
		self.currentUTCTimeStamp = datetime.now(timezone.utc).timestamp() * 1000;

	def __del__(self):
		pass;
		#print(self.currentUTC)
		
	def time(self):
		pass;

	def today(self):
		return time.strftime("%d-%m-%Y");
	
	
