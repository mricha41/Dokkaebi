#sending messages with Dokkaebi
#detailed example demonstrating
#many of the parameters available
#when sending messages

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
	'url': config["Telegram"]["WEBHOOK_URL"]
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

			if "reply_to_message" in data["message"]:
				if data["message"]["reply_to_message"]["from"]["username"] == self.bot_info["username"]:
					print(self.sendMessage({"chat_id": chat_id, "text": "Thanks for picking - " + data["message"]["text"]}).json())
			else:
				if command in ["/start", "/start@" + self.bot_info["username"]]:
					msg = {
						"chat_id": chat_id,
						"text": "Thanks for using "  + self.bot_info["username"] + ", " + user_first_name + "!"
					}
					print(self.sendMessage(msg).json())
				elif command in ["/link", "/link@" + self.bot_info["username"]]:
					#see the formatting example for more
					#html/markdown examples
					msg = {
						"chat_id": chat_id,
						"text": "here's <a href=\"https://github.com/mricha41/Dokkaebi\">a link</a> to the Dokkaebi github repo.",
						"disable_web_page_preview": True,
						"parse_mode": "html",
						"disable_notification": True
					}
					print(self.sendMessage(msg).json())
				elif command in ["/reply", "/reply@" + self.bot_info["username"]]:
					reply_id = data["message"]["message_id"]
					self.sendMessage({
						"chat_id": chat_id,
						"text": "I see you sent me something - here's something back at ya!",
						"reply_to_message_id": reply_id
					})
				elif command in ["/replyoptions", "/replyoptions@" + self.bot_info["username"]]:
					reply_id = data["message"]["message_id"]
					print(self.sendMessage({
						"chat_id": chat_id,
						"text": "I see you sent me something - here's something back at ya!",
						"reply_to_message_id": reply_id,
						"reply_markup": {
							"keyboard": [
								["option 1"],
								["option 2"],
								["option 3"],
								["option 4"]
							],
							"one_time_keyboard": True
						}
					}).json())
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