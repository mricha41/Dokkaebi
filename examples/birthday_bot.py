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
	#members
	command = None
	last_reply_id = 0
	
	def handleData(self, data):
		print(data)
		"""
		{
			'update_id': 840426172, 
			'message': {
				'message_id': 1145, 
				'from': {
					'id': 773890555, 
					'is_bot': False, 
					'first_name': 'Butcher', 
					'last_name': 'Pete', 
					'language_code': 'en'
				}, 
				'chat': {
					'id': 773890555, 
					'first_name': 
					'Butcher', 
					'last_name': 'Pete', 
					'type': 'private'
				}, 
				'date': 1599618177, 
				'text': 'October'
			}
		}
		{
			'ok': True, 
			'result': {
				'message_id': 1144, 
				'from': {
					'id': 1176480601, 
					'is_bot': True, 
					'first_name': 'BirthdayBot3K', 
					'username': 'Birthday3KBot'
				}, 
				'chat': {
					'id': 773890555, 
					'first_name': 'Butcher', 
					'last_name': 'Pete', 
					'type': 'private'
				}, 
				'date': 1599618162, 
				'reply_to_message': {
					'message_id': 1143, 
					'from': {
						'id': 773890555, 
						'is_bot': False, 
						'first_name': 'Butcher', 
						'last_name': 'Pete', 
						'language_code': 'en'
					}, 
					'chat': {
						'id': 773890555, 
						'first_name': 'Butcher', 
						'last_name': 'Pete', 
						'type': 'private'
					}, 
					'date': 1599618161, 
					'text': '/birthday', 
					'entities': [{'offset': 0, 'length': 9, 'type': 'bot_command'}]
				}, 
				'text': 'Select a month, Butcher.'
			}
		}
		{
			'update_id': 840426171, 
			'message': {
				'message_id': 1143, 
				'from': {
					'id': 773890555, 
					'is_bot': False, 
					'first_name': 'Butcher', 
					'last_name': 'Pete', 
					'language_code': 'en'
				}, 
				'chat': {
					'id': 773890555, 
					'first_name': 'Butcher', 
					'last_name': 'Pete', 
					'type': 'private'
				}, 
				'date': 1599618161, 
				'text': '/birthday', 
				'entities': [{'offset': 0, 'length': 9, 'type': 'bot_command'}]
			}
		}
		"""
		if "entities" in data["message"] and data["message"]["entities"][0]["type"] == "bot_command":
			#it's a command, so process it as such
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
					}).json())
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
				elif command in ["/birthday", "/birthday@" + self.bot_info["username"]]:
					reply_id = data["message"]["message_id"]
					print(self.sendMessage({
						"chat_id": chat_id,
						"text": "Select a month, " + user_first_name + ".",
						"reply_to_message_id": reply_id,
						"reply_markup": {
							"keyboard": [
								["January"],
								["February"],
								["March"],
								["April"],
								["May"],
								["June"],
								["July"],
								["August"],
								["September"],
								["October"],
								["November"],
								["December"]
							],
							"one_time_keyboard": True
						}
					}).json())

					self.last_reply_id = reply_id + 1
					print("reply id: {}".format(reply_id))
					print("last reply id: {}".format(self.last_reply_id))

		else:
			#check for a reply, since it's not a command
			if self.last_reply_id and self.last_reply_id != None:
				looking_for_reply_id = self.last_reply_id + 1
				print("last reply id: {}".format(self.last_reply_id))
				print("looking for id: {}".format(looking_for_reply_id))
				print("actual id: {}".format(data["message"]["message_id"]))
				if int(data["message"]["message_id"]) == looking_for_reply_id:#and "message" in data and "text" in data["message"]:
					selected_month = data["message"]["text"]
					print(selected_month)
				else:
					print("Not a reply to /birthday")
			else:
				print("Not a reply to /birthday")

	def onInit(self):
		self.setMyCommands(bot_commands)
		self.getMyCommands()

newBot = Bot(hook_data)