#birthday bot example

#if you don't whish to set this
#just copy the file to the top-level
#folder and run it there w/out this
import sys
sys.path.append("../dokkaebi")
print(sys.path)

import string

import requests
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
	'hostname': config["Telegram"]["HOSTNAME"], 
	'port': int(config["Telegram"]["PORT"]), 
	'token': config["Telegram"]["BOT_TOKEN"], 
	'url': config["Telegram"]["WEBHOOK_URL"],
	'environment': config["Telegram"]["ENVIRONMENT"]
}

#you can actually store more data
#in your bot command payload
#here, i put an example in with
#each command to illustrate its use
#keep in mind that Telegram will drop
#the extra fields when it stores it, so use
#this copy of the data for example storeage/retrieval
bot_commands = {
	"commands": [
		{'command': 'start', 'description': 'starts the bot.', 'example': "Just issue /start in the Telegram message box."}
	]
}

class Bot(dokkaebi.Dokkaebi):
	def handleData(self, data):
		print(data)
		command = None
		if "message" in data:
			if "text" in data["message"]:
				#this will work both for single word commands
				#and multi-word commands
				command = data["message"]["text"].split(' ')[0] #grab command keyword...
				user_parameters = ""
				if data["message"]["text"].split(' ')[1:]:
					user_parameters = data["message"]["text"].split(' ')[1:] #get the rest of the user's text...
			else:
				command = None

			chat_id = data["message"]["chat"]["id"]
			user_first_name = data["message"]["from"]["first_name"]
			
			if command in ["/start", "/start@" + self.bot_info["username"]]:
				#for fun!
				hbd = "https://external-content.duckduckgo.com/iu/?u=https://www.happybirthdaycake2015.com/wp-content/uploads/2018/05/Funny-Happy-Birthday-Dance-Gif-6.gif&f=1&nofb=1"
				self.sendAnimation({"chat_id": chat_id, "animation": hbd})
				msg = {
					"chat_id": chat_id,
					"text": "Thanks for using "  + self.bot_info["username"] + ", " + user_first_name + "!\n" + "&#128513;",
					"parse_mode": "html"
				}
				print(self.sendMessage(msg).json())
				print(self.sendMessage({
					"chat_id": chat_id, 
					"text": "Just submit a command to use" + self.bot_info["username"] + ".\nUse the /help command for the full list of commands."
				}))
			elif command in ["/help", "/help@" + self.bot_info["username"]]:
				#append the help string from
				#the bot_command data structure
				t = ""
				for x in bot_commands["commands"]:
					t += "".join("/" + x["command"] + " - " + x["description"] + "\nExample: " + x["example"]) + "\n"
				
				msg = {
					"chat_id": chat_id,
					"text": "The following commands are available: \n" + t.rstrip(),
					"parse_mode": "html"
				}
				
				#print(t.rstrip())
				self.sendMessage(msg)
		
	def onInit(self):
		self.setMyCommands(bot_commands)
		self.getMyCommands()

newBot = Bot(hook_data)