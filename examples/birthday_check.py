import sys
sys.path.append("../dokkaebi")
print(sys.path)

import requests
import json
import sqlite3
import schedule
import time
from datetime import date

from dokkaebi import dokkaebi
from configparser import ConfigParser

#appending to sys.path allows
#config to be read relative to that path
#even though this file is in the examples folder
config = ConfigParser()
config.read('birthday_bot.ini')

#be sure to cast anything that shouldn't
#be a string - reading the .ini file
#seems to result in strings for every item read.
hook_data = {
	'token': config["Telegram"]["BOT_TOKEN"]
}

months = ["January","February","March",
			"April","May","June",
			"July","August","September",
			"October","November","December"]

print(date.today().month)
print(date.today().day)

class CheckBirthdays(dokkaebi.Dokkaebi):
	def happyBirthday(self):
		#do birthday stuff...
		with open('data/bday.json', 'r', encoding='utf-8') as f:
			bday = json.load(f)
		#print(bday)
		found = False
		for key,value in bday.items():
			#print(value)
			#print(months[date.today().month - 1])
			#print(str(date.today().day))
			#print(value["month"])
			#print(value["day"])

			if months[date.today().month - 1] == value["month"] and str(date.today().day) == value["day"]:
				found = True
				if "user_last_name" in value:
					print(self.sendMessage({"chat_id": value["chat_id"], "text": "Happy birthday, @" + value["user_first_name"] + value["user_last_name"] + "!!!"}).json())
				else:
					print(self.sendMessage({"chat_id": value["chat_id"], "text": "Happy birthday, @" + value["user_first_name"] + "!!!"}).json())
			
		if found:
			print("Birthday messages sent.")
		else:
			print("No birthdays found.")

hbd = CheckBirthdays(hook_data)

schedule.every().day.at('20:00').do(hbd.happyBirthday)

while True:
	schedule.run_pending()
	time.sleep(1)