#sending media messages with Dokkaebi
#detailed example demonstrating
#many of the parameters available
#when sending media messages

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
			
			if command in ["/start", "/start@" + self.bot_info["username"]]:
				msg = {
					"chat_id": chat_id,
					"text": "Thanks for using "  + self.bot_info["username"] + ", " + user_first_name + "!"
				}
				print(self.sendMessage(msg).json())
			elif command in ["/cat", "/cat@" + self.bot_info["username"]]:
				photo = {
					"chat_id": chat_id,
					"photo": "https://i.ytimg.com/vi/2fb-g_V-UT4/hqdefault.jpg",
					"caption": "Silly cat face \\- *so* _funny_\\!",
					"parse_mode": "MarkdownV2"
				}
				print(self.sendPhoto(photo).json())
			elif command in ["/bark", "/bark@" + self.bot_info["username"]]:
				print(self.sendAudio({
					"chat_id": chat_id, 
					"audio": "http://www.orangefreesounds.com/wp-content/uploads/2015/07/Dog-barking-mp3.mp3",
					"caption": "A barking dog. <i>Aggressively</i> barking.",
					"parse_mode": "html",
					"duration": 10,
					"performer": "Dog",
					"title": "Dog-barking-mp3",
					"thumb": {"thumb": open("uploadables/thumbnail.jpg", "rb")}
				}).json())
			elif command in ["/cheatsheet", "/cheatsheet@" + self.bot_info["username"]]:
				print(self.sendDocument({
					"chat_id": chat_id, 
					"document": "https://static.realpython.com/python-cheat-sheet.pdf",
					"thumb": {"thumb": open("uploadables/thumbnail.jpg", "rb")},
					"caption": "Python <u>cheat sheet</u>",
					"parse_mode": "html"
				}).json())
			elif command in ["/jump", "/jump@" + self.bot_info["username"]]:
				print(self.sendVideo({
					"chat_id": chat_id, 
					"video": "https://media.vlipsy.com/vlips/bOTh8qyT/480p.mp4",
					"duration": 8,
					"width": 400,
					"height": 400,
					"thumb": {"thumb": open("uploadables/thumbnail.jpg", "rb")},
					"caption": "~Grumpy~Jumpy cat",
					"parse_mode": "MarkdownV2",
					"supports_streaming": False
				}).json())
			elif command in ["/laugh", "/laugh@" + self.bot_info["username"]]:
				print(self.sendAnimation({
					"chat_id": chat_id, 
					"animation": "https://media.tenor.com/images/5cb1114e4f1a94c33812a2c332da0c3a/tenor.gif",
					"duration": 3,
					"width": 400,
					"height": 400,
					"thumb": {"thumb": open("uploadables/thumbnail.jpg", "rb")},
					"caption": "*Hmmf\\.\\.\\.*hahaha\\!",
					"parse_mode": "MarkdownV2"
				}).json())
			elif command in ["/monkey", "/monkey@" + self.bot_info["username"]]:
				print(self.sendVoice({
					"chat_id": chat_id,
					"voice": "https://freesound.org/data/previews/458/458396_8552979-lq.ogg",
					"caption": "Monkey business",
					#"parse_mode": "MarkdownV2"
					"duration": 1
				}).json())
			elif command in ["/memo", "/memo@" + self.bot_info["username"]]:
				print(self.sendVideoNote({
					"chat_id": chat_id, 
					"video_note": "https://media.vlipsy.com/vlips/a8cOiDDD/480p.mp4",
					"duration": 6,
					"length": 200,
					"thumb": {"thumb": open("uploadables/thumbnail.jpg", "rb")}
				}).json())
			elif command in ["/cats", "/cats@" + self.bot_info["username"]]:
				group = {
					"chat_id": chat_id,
					"media": [
						{"type": "photo", "media": "https://i.ytimg.com/vi/Cw3cZiyeJOA/hqdefault.jpg"},
						{"type": "photo", "media": "https://i.ytimg.com/vi/2fb-g_V-UT4/hqdefault.jpg"},
						{"type": "photo", "media": "https://media.npr.org/assets/img/2019/05/17/gettyimages-611696954_wide-7ccf1c1dbd6bf693f32364d6a0cd1b92c554859a.jpg"}
					]
				}
				print(self.sendMediaGroup(group).json())
			elif command in ["/funnycats", "/funnycats@" + self.bot_info["username"]]:
				group = {
					"chat_id": chat_id,
					"media": [
						{"type": "video", "media": "https://media.vlipsy.com/vlips/zWlPtKSs/480p.mp4"},
						{"type": "video", "media": "https://media.vlipsy.com/vlips/bOTh8qyT/480p.mp4"},
						{"type": "video", "media": "https://media.vlipsy.com/vlips/IMFJFs6r/480p.mp4"}
					]
				}
				print(self.sendMediaGroup(group).json())
			else:
				msg = {
					"chat_id": chat_id,
					"text": "I didn't quite get that, " + user_first_name + ". Please try a valid command."
				}
				print(self.sendMessage(msg).json())
		
	def onInit(self):
		self.setMyCommands(bot_commands)
		self.getMyCommands()

newBot = Bot(hook_data)