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
	'url': config["Telegram"]["WEBHOOK_URL"]
}

bot_commands = {
	"commands": [
		{'command': 'start', 'description': 'starts the bot.'}
	]
}

class Bot(dokkaebi.Dokkaebi):
	def handleData(self, data):
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
			self.sendMessage(msg)
		elif command in ["/roll", "/roll@" + self.bot_info["username"]]:
			self.sendDice({"chat_id": chat_id})
		elif command in ["/cat", "/cat@" + self.bot_info["username"]]:
			photo = {
				"chat_id": chat_id,
				"photo": "https://i.ytimg.com/vi/2fb-g_V-UT4/hqdefault.jpg"
			}
			self.sendPhoto(photo)
		elif command in ["/bark", "/bark@" + self.bot_info["username"]]:
			self.sendAudio({"chat_id": chat_id, "audio": "https://tunelilu.com/pr2/Barking_Dog.mp3"})
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