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
			#kick/unban/restrict/promote actions require specific conditions
			#be met and only work in certain types of chats - see the Telegram
			#API doc for full details. call the function and inspect the error
			#information in the returned json object for more information too.
			elif command in ["/kick", "/kick@" + self.bot_info["username"]]:
				print(self.kickChatMember({"chat_id": chat_id, "user_id": None}).json()) #provide your own user_id
			elif command in ["/unkick", "/unkick@" + self.bot_info["username"]]:
				print(self.unbanChatMember({"chat_id": chat_id, "user_id": None}).json()) #provide your own user_id
			elif command in ["/restrict", "/restrict@" + self.bot_info["username"]]:
				print(self.restrictChatMember({
					"chat_id": chat_id, 
					"user_id": None, 
					"permissions": {
						"can_send_messages": True,
						"can_send_media_messages": True,
						"can_send_polls": True,
						"can_send_other_messages": True,
						"can_add_web_page_previews": True,
						"can_change_info": True,
						"can_invite_users":	True,
						"can_pin_messages":	True,
					}
				}).json()) #provide your own user_id
			elif command in ["/promote", "/promote@" + self.bot_info["username"]]:
				print(self.promoteChatMember({
					"chat_id": chat_id, 
					"user_id": None,
					"can_change_info": True,
					"can_post_messages": True,
					"can_edit_messages": True,
					"can_delete_messages": True,
					"can_invite_users": True,
					"can_restrict_members": True,
					"can_pin_messages": True,
					"can_promote_members": True
				}).json()) #provide your own user_id
			elif command in ["/admintitle", "/admintitle@" + self.bot_info["username"]]:
				#only works in supergroups - call it in another type
				#of chat to view the error information in the json object
				print(self.setChatAdministratorCustomTitle({
					"chat_id": chat_id, 
					"user_id": self.bot_info["id"],
					"custom_title": "Mr. Bot Person"
				}).json())
			elif command in ["/chatpermissions", "/chatpermissions@" + self.bot_info["username"]]:
				print(self.setChatPermissions({
					#permissions set do not apply to admins
					#in the way they apply to normal users
					#this is not obvious until you open a 
					#client and observe the impact the
					#changes have firsthand - just a warning!
					"chat_id": chat_id,
					"permissions": {
						"can_send_messages": False,
						"can_send_media_messages": False,
						"can_send_polls": False,
						"can_send_other_messages": False,
						"can_add_web_page_previews": False,
						"can_change_info": False,
						"can_invite_users":	False,
						"can_pin_messages":	False,
					}
				}).json())
			elif command in ["/chatlink", "/chatlink@" + self.bot_info["username"]]:
				#export the chat link...
				link = self.exportChatInviteLink({
					"chat_id": chat_id 
				}).json()
				#do something useful with it, like send it to
				#chat members!
				self.sendMessage({"chat_id": chat_id, "text": link["result"]})
			elif command in ["/setchatphoto", "/setchatphoto@" + self.bot_info["username"]]:
				#this doesn't work, unfortunately...
				#print(self.setChatPhoto({"chat_id": chat_id, "photo": "https://i.ytimg.com/vi/Cw3cZiyeJOA/hqdefault.jpg"}).json())
				
				#what needs to happen is to upload a file opened locally
				#and send it to Telegram...
				cat = "uploadables/small_face_cat.jpg"
				print(self.setChatPhoto({"chat_id": chat_id}, {"photo": open(cat, "rb")}).json())
			elif command in ["/deletechatphoto", "/deletechatphoto@" + self.bot_info["username"]]:
				print(self.deleteChatPhoto({"chat_id": chat_id}).json())
			elif command in ["/chattitle", "/chattitle@" + self.bot_info["username"]]:
				print(self.setChatTitle({"chat_id": chat_id, "title": "Bot Testing Sandbox"}).json())
			elif command in ["/chatdesc", "/chatdesce@" + self.bot_info["username"]]:
				print(self.setChatDescription({"chat_id": chat_id, "description": "tom-foolery"}).json())
			elif command in ["/leave", "/leave@" + self.bot_info["username"]]:
				print(self.leaveChat({"chat_id": chat_id}).json())
			elif command in ["/pin", "/pin@" + self.bot_info["username"]]:
				print(self.pinChatMessage({"chat_id": chat_id, "message_id": 26}).json())
			elif command in ["/unpin", "/unpin@" + self.bot_info["username"]]:
				print(self.unpinChatMessage({"chat_id": chat_id}).json())
			elif command in ["/setstickers", "/setstickers@" + self.bot_info["username"]]:
				#only works for supergroups - call anyway to see what the error shows
				print(self.setChatStickerSet({"chat_id": chat_id, "sticker_set_name": "Fallout"}).json())
			elif command in ["/deletestickers", "/deletestickers@" + self.bot_info["username"]]:
				#only works for supergroups - call anyway to see what the error shows
				print(self.deleteChatStickerSet({"chat_id": chat_id}).json())
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