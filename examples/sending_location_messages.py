#sending location messages with Dokkaebi
#detailed example demonstrating
#many of the parameters available
#when sending location messages

#if you don't whish to set this
#just copy the file to the top-level
#folder and run it there w/out this
import sys
sys.path.append("../dokkaebi")
print(sys.path)

from dokkaebi import dokkaebi
from configparser import ConfigParser

#appending to sys.path allows
#config to be read relative to that path
#even though this file is in the examples folder
config = ConfigParser()
config.read('config.ini')

#be sure to cast anything that shouldn't
#be a string - reading the .ini file
#seems to result in strings for every item read.
hook_data = {
	'hostname': config["Telegram"]["HOSTNAME"], 
	'port': int(config["Telegram"]["PORT"]), 
	'token': config["Telegram"]["BOT_TOKEN"], 
	'url': config["Telegram"]["WEBHOOK_URL"],
	'environment': config["Telegram"]["ENVIRONMENT"]
}

bot_commands = {
	"commands": [
		{'command': 'start', 'description': 'starts the bot.'}
	]
}

class Bot(dokkaebi.Dokkaebi):
	def handleData(self, data):
		print(data)
		if "message" in data:
			if "text" in data["message"]:
				command = data["message"]["text"]
			else:
				command = ""

			chat_id = data["message"]["chat"]["id"]
			user_first_name = data["message"]["from"]["first_name"]
			
			if command in ["/start", "/start@" + self.bot_info["username"]]:
				msg = {
					"chat_id": chat_id,
					"text": "Thanks for using "  + self.bot_info["username"] + ", " + user_first_name + "!"
				}
				print(self.sendMessage(msg).json())
			elif command in ["/findme", "/findme@" + self.bot_info["username"]]:
				location = {
					"chat_id": chat_id,
					"latitude": 19.741755,
					"longitude": -155.844437,
					"live_period": 240 #keep alive long enough to make an edit - adjust as necessary
				}
				
				self.last_location_message = self.sendLocation(location).json()["result"]
				print(self.last_location_message["message_id"])
			elif command in ["/findmenow", "/findmenow@" + self.bot_info["username"]]:
				location = {
					"chat_id": chat_id,
					"message_id": int(self.last_location_message["message_id"]),
					"latitude": 1.924992,
					"longitude": 73.399658
				}
				self.editMessageLiveLocation(location)
			elif command in ["/dontfindme", "/dontfindme@" + self.bot_info["username"]]:
				location = {
					"chat_id": chat_id,
					"message_id": int(self.last_location_message["message_id"])
				}
				self.stopMessageLiveLocation(location)
			elif command in ["/venue", "/venue@" + self.bot_info["username"]]:
				venue = {
					"chat_id": chat_id,
					"latitude": 33.755556,
					"longitude": -84.4,
					"title": "Mercedes-Benz Stadium - Atlanta",
					"address": "1 AMB Drive NW Atlanta, GA 30313"
				}
				self.sendVenue(venue)
			else:
				msg = {
					"chat_id": chat_id,
					"text": "I didn't quite get that, " + user_first_name + ". Please try a valid command."
				}
				self.sendMessage(msg)
		
	def onInit(self):
		self.setMyCommands(bot_commands)
		self.getMyCommands()

newBot = Bot(hook_data)