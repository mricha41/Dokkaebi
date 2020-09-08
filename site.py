#one gigantic, monolithic example of most of
#the API wrapper. see https://core.telegram.org/bots/api#available-methods
#for the complete list and some insight on
#how the wrapper works

from dokkaebi import dokkaebi
from configparser import ConfigParser
import requests

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
			elif command in ["/roll", "/roll@" + self.bot_info["username"]]:
				self.sendDice({"chat_id": chat_id})
			elif command in ["/cat", "/cat@" + self.bot_info["username"]]:
				photo = {
					"chat_id": chat_id,
					"photo": "https://i.ytimg.com/vi/2fb-g_V-UT4/hqdefault.jpg"
				}
				self.sendPhoto(photo)
			elif command in ["/bark", "/bark@" + self.bot_info["username"]]:
				self.sendAudio({"chat_id": chat_id, "audio": "http://www.orangefreesounds.com/wp-content/uploads/2015/07/Dog-barking-mp3.mp3"})
			elif command in ["/cheatsheet", "/cheatsheet@" + self.bot_info["username"]]:
				self.sendDocument({"chat_id": chat_id, "document": "https://static.realpython.com/python-cheat-sheet.pdf"})
			elif command in ["/jump", "/jump@" + self.bot_info["username"]]:
				self.sendVideo({"chat_id": chat_id, "video": "https://media.vlipsy.com/vlips/bOTh8qyT/480p.mp4"})
			elif command in ["/laugh", "/laugh@" + self.bot_info["username"]]:
				self.sendAnimation({"chat_id": chat_id, "animation": "https://media.tenor.com/images/5cb1114e4f1a94c33812a2c332da0c3a/tenor.gif"})
			elif command in ["/monkey", "/monkey@" + self.bot_info["username"]]:
				self.sendVoice({"chat_id": chat_id, "voice": "https://freesound.org/data/previews/458/458396_8552979-lq.ogg"})
			elif command in ["/memo", "/memo@" + self.bot_info["username"]]:
				self.sendVideoNote({"chat_id": chat_id, "video_note": "https://media.vlipsy.com/vlips/a8cOiDDD/480p.mp4"})
			elif command in ["/cats", "/cats@" + self.bot_info["username"]]:
				group = {
					"chat_id": chat_id,
					"media": [
						{"type": "photo", "media": "https://i.ytimg.com/vi/Cw3cZiyeJOA/hqdefault.jpg"},
						{"type": "photo", "media": "https://i.ytimg.com/vi/2fb-g_V-UT4/hqdefault.jpg"},
						{"type": "photo", "media": "https://media.npr.org/assets/img/2019/05/17/gettyimages-611696954_wide-7ccf1c1dbd6bf693f32364d6a0cd1b92c554859a.jpg"}
					]
				}
				self.sendMediaGroup(group)
			elif command in ["/funnycats", "/funnycats@" + self.bot_info["username"]]:
				group = {
					"chat_id": chat_id,
					"media": [
						{"type": "video", "media": "https://media.vlipsy.com/vlips/zWlPtKSs/480p.mp4"},
						{"type": "video", "media": "https://media.vlipsy.com/vlips/bOTh8qyT/480p.mp4"},
						{"type": "video", "media": "https://media.vlipsy.com/vlips/IMFJFs6r/480p.mp4"}
					]
				}
				self.sendMediaGroup(group)
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
			elif command in ["/contact", "/contact@" + self.bot_info["username"]]:
				contact = {
					"chat_id": chat_id,
					"phone_number": "555-5555",
					"first_name": "Charles",
					"last_name": "In Charge",
					"vcard": "BEGIN:VCARD" #for example - Telegram doesn't appear to use it for anything though
						   + "VERSION:4.0"
						   + "N:Gump;Forrest;;Mr.;"
						   + "FN:Forrest Gump"
						   + "ORG:Bubba Gump Shrimp Co."
						   + "TITLE:Shrimp Man"
						   + "PHOTO;MEDIATYPE=image/gif:http://www.example.com/dir_photos/my_photo.gif"
						   + "TEL;TYPE=work,voice;VALUE=uri:tel:+1-111-555-1212"
						   + "TEL;TYPE=home,voice;VALUE=uri:tel:+1-404-555-1212"
						   + "ADR;TYPE=WORK;PREF=1;LABEL=\"100 Waters Edge\nBaytown\, LA 30314\nUnited States of America\":;;100 Waters Edge;Baytown;LA;30314;United States of America"
						   + "ADR;TYPE=HOME;LABEL=\"42 Plantation St.\nBaytown\, LA 30314\nUnited States of America\":;;42 Plantation St.;Baytown;LA;30314;United States of America"
						   + "EMAIL:forrestgump@example.com"
						   + "REV:20080424T195243Z"
						   + "x-qq:21588891"
						   + "END:VCARD"
				}
				self.sendContact(contact)
			elif command in ["/venue", "/venue@" + self.bot_info["username"]]:
				venue = {
					"chat_id": chat_id,
					"latitude": 33.755556,
					"longitude": -84.4,
					"title": "Mercedes-Benz Stadium - Atlanta",
					"address": "1 AMB Drive NW Atlanta, GA 30313"
				}
				self.sendVenue(venue)
			elif command in ["/poll", "/poll@" + self.bot_info["username"]]:
				#pay attention to the console when chat
				#members respond to the poll/quiz - you
				#will receive data from Telegram as responses
				#are given - handle that data accordingly
				poll = {
					"chat_id": chat_id,
					"question": "How much wood can a woodchuck chuck?",
					"options": ["2", "7", "A lot", "None"],
					"correct_option_id": 0,
					"explanation": "Cause woodchucks can chuck some wood. Just not a lot of wood."#,
					#"is_closed": True
				}
				self.sendPoll(poll)
			elif command in ["/action", "/action@" + self.bot_info["username"]]:
				self.sendChatAction({
					"chat_id": chat_id,
					"action": "typing"
				})
			elif command in ["/userphotos", "/userphotos@" + self.bot_info["username"]]:
				#returns json info to console, it's up to you
				#what you do with the info once it's returned
				#(set profile photo, set chat photo, etc.)
				print(self.getUserProfilePhotos({
					"user_id": self.bot_info["id"]
				}).json())
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
			elif command in ["/getchat", "/getchat@" + self.bot_info["username"]]:
				print(self.getChat({"chat_id": chat_id}).json())
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
			elif command in ["/getchat", "/getchat@" + self.bot_info["username"]]:
				print(self.getChat({"chat_id": chat_id}).json())
			elif command in ["/pin", "/pin@" + self.bot_info["username"]]:
				print(self.pinChatMessage({"chat_id": chat_id, "message_id": 692}).json())
			elif command in ["/unpin", "/unpin@" + self.bot_info["username"]]:
				print(self.unpinChatMessage({"chat_id": chat_id}).json())
			elif command in ["/admins", "/admins@" + self.bot_info["username"]]:
				print(self.getChatAdministrators({"chat_id": chat_id}).json())
			elif command in ["/count", "/count@" + self.bot_info["username"]]:
				count = self.getChatMembersCount({"chat_id": chat_id}).json()
				print(count)
				self.sendMessage({"chat_id": chat_id, "text": "Members in chat: {}".format(count["result"])})
			elif command in ["/getmember", "/getmember@" + self.bot_info["username"]]:
				print(self.getChatMember({"chat_id": chat_id, "user_id": self.bot_info["id"]}).json())
			elif command in ["/setstickers", "/setstickers@" + self.bot_info["username"]]:
				#only works for supergroups - call anyway to see what the error shows
				print(self.setChatStickerSet({"chat_id": chat_id, "sticker_set_name": "Holy Poop"}).json())
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