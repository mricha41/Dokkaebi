#managing chats with Dokkaebi
#detailed example demonstrating
#many of the available methods
#for managing chats with bots

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
			elif command in ["/getchat", "/getchat@" + self.bot_info["username"]]:
				res = self.getChat({"chat_id": chat_id}).json()
				print(res)
				print(self.sendMessage({"chat_id": chat_id, "text": "chat data: {}".format(res["result"])}).json())
			elif command in ["/admins", "/admins@" + self.bot_info["username"]]:
				admins = self.getChatAdministrators({"chat_id": chat_id}).json()
				print(self.sendMessage({"chat_id": chat_id, "text": "admins: {}".format(admins)}).json())
			elif command in ["/count", "/count@" + self.bot_info["username"]]:
				count = self.getChatMembersCount({"chat_id": chat_id}).json()
				print(count)
				print(self.sendMessage({"chat_id": chat_id, "text": "Members in chat: {}".format(count["result"])}).json())
			elif command in ["/getmember", "/getmember@" + self.bot_info["username"]]:
				member = self.getChatMember({"chat_id": chat_id, "user_id": self.bot_info["id"]}).json()
				print(self.sendMessage({"chat_id": chat_id, "text": "member info: {}".format(member)}).json())
			elif command in ["/userphotos", "/userphotos@" + self.bot_info["username"]]:
				#returns json info to console, it's up to you
				#what you do with the info once it's returned
				#(set profile photo, set chat photo, etc.)
				photos = self.getUserProfilePhotos({
					"user_id": self.bot_info["id"]
				}).json()
				print(self.sendMessage({"chat_id": chat_id, "text": "photos: {}".format(photos)}).json())
			elif command in ["/getfile", "/getfile@" + self.bot_info["username"]]:
				#grab the file id for the first profile photo set for the bot
				file_id = self.getUserProfilePhotos({"user_id": self.bot_info["id"]}).json()["result"]["photos"][0][0]["file_id"]
				#print(file_id)
				#use get file to get the file by file_id...
				file = self.getFile({
					"file_id": file_id
				}).json()

				#use the File json object in some kind of
				#"useful" way :D
				self.sendPhoto({
					"chat_id": chat_id,
					"photo": file["result"]["file_id"]
				})
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