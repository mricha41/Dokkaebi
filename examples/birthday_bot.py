#birthday bot example

#if you don't whish to set this
#just copy the file to the top-level
#folder and run it there w/out this
import sys
sys.path.append("../dokkaebi")
print(sys.path)

import string
import json
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

days = [["1"],["2"],["3"],["4"],["5"],
		["6"],["7"],["8"],["9"],["10"],
		["11"],["12"],["13"],["14"],["15"],
		["16"],["17"],["18"],["19"],["20"],
		["21"],["22"],["23"],["24"],["25"],
		["26"],["27"],["28"],["29"],["30"],["31"]]

months = [["January"],["February"],["March"],
			["April"],["May"],["June"],
			["July"],["August"],["September"],
			["October"],["November"],["December"]]

class Bot(dokkaebi.Dokkaebi):
	#members
	command = None
	last_reply_id = 0
	
	def handleData(self, data):

		print(data)

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
							"keyboard": months,
							"one_time_keyboard": True
						}
					}).json())

					self.last_reply_id = reply_id + 1
					print("reply id: {}".format(reply_id))
					print("last reply id: {}".format(self.last_reply_id))

		else:
			#check for a reply, since it's not a command
			chat_id = data["message"]["chat"]["id"]
			if "first_name" in data["message"]["from"]:
				user_first_name = data["message"]["from"]["first_name"]
			else:
				user_first_name = ""
			if "last_name" in data["message"]["from"]:
				user_last_name = data["message"]["from"]["last_name"]
			else:
				user_last_name = ""

			if self.last_reply_id and self.last_reply_id != None:
				looking_for_reply_id = self.last_reply_id + 1
				print("last reply id: {}".format(self.last_reply_id))
				print("looking for id: {}".format(looking_for_reply_id))
				print("actual id: {}".format(data["message"]["message_id"]))
				if int(data["message"]["message_id"]) == looking_for_reply_id: #first reply with a month...
					user_id = data["message"]["from"]["id"]
					selected_month = data["message"]["text"]
					#print(selected_month)

					#load it first to check records...
					with open('data/bday.json', 'r', encoding='utf-8') as f:
						bday = json.load(f)

					#update it if it already exists...
					if bday.get(str(user_id)):
						bday[str(user_id)]["month"] = selected_month
						#write it out to the file
						with open('data/bday.json', mode='w', encoding='utf-8') as f:
							json.dump(bday, f, indent=2)

					#otherwise we need a new bday record
					else:
						new_bday = {
							str(user_id) : {
								"chat_id": chat_id,
								"user_first_name": user_first_name,
								"user_last_name": user_last_name,
								"month": selected_month,
								"day": ""
							}
						}
						#append it to the file
						with open('data/bday.json', mode='w', encoding='utf-8') as f:
							bday.update(new_bday)
							json.dump(bday, f, indent=2)

					#okay...now we'll ask for a day
					print(self.sendMessage({
						"chat_id": chat_id,
						"text": "Select a month, " + user_first_name + ".",
						"reply_to_message_id": looking_for_reply_id,
						"reply_markup": {
							"keyboard": days,
							"one_time_keyboard": True
						}
					}).json())
				elif int(data["message"]["message_id"]) == (looking_for_reply_id + 2): #second reply with a day...
					user_id = data["message"]["from"]["id"]
					selected_day = data["message"]["text"]
					#print(selected_day)

					#load data...
					with open('data/bday.json', 'r', encoding='utf-8') as f:
						bday = json.load(f)
						
					#overwrite the previous (possibly blank) value
					bday[str(user_id)]["day"] = selected_day

					#dump it back in the file
					with open('data/bday.json', 'w', encoding='utf-8') as f:
						json.dump(bday, f, indent=2)

					print(self.sendMessage({
						"chat_id": chat_id,
						"text": "Thanks for using " + self.bot_info["username"] + "," + user_first_name + "!\nYou'll receive a notification on your birthday. Stay tuned &#128513;",
						"parse_mode": "html"
					}).json())
				else:
					print("Not a reply to /birthday")
			else:
				print("Possible reply, not a reply to /birthday")

	def onInit(self):
		self.setMyCommands(bot_commands)
		self.getMyCommands()

newBot = Bot(hook_data)