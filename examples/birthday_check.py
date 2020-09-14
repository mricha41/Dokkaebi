import sys
sys.path.append("../dokkaebi")
print(sys.path)

import requests
import json
import sqlite3
import schedule
import time

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

class CheckBirthdays(dokkaebi.Dokkaebi):
	def happyBirthday(self):
		#do birthday stuff...
		with open('data/bday.json', 'r', encoding='utf-8') as f:
			bday = json.load(f)
		print(bday)
		print(self.sendMessage({"chat_id": bday["chat_id"], "text": "Happy birthday, " + bday["user_first_name"] + "!!!"}).json())

hbd = CheckBirthdays(hook_data)

schedule.every().minute.do(hbd.happyBirthday)

while True:
	schedule.run_pending()
	time.sleep(1)