import datetime, os, json, time
from datetime import datetime, date, timedelta, timezone

class Time:
	def __init__(self):
		self.currentUTC = datetime.now(timezone.utc);
		self.currentUTCTimeStamp = datetime.now(timezone.utc).timestamp() * 1000;

	def __del__(self):
		pass;
		#print(self.currentUTC)
		
	def time(self):
		pass;
	
	def UTCNow(self):
		return datetime.now(timezone.utc);
	
	def str_todaytime(self) -> str:
		return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	def today(self):
		return time.strftime("%d-%m-%Y");
	
	
