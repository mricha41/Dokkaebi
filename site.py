from dokkaebi import dokkaebi
from configparser import ConfigParser

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
		command = data["message"]["text"]
		if(command in ["/start", "/start@" + self.bot_info["username"]]):
			self.sendMessage("Thanks for using "  + self.bot_info["username"] + ", " + self.message_from_info["first_name"] + "!")
		elif(command in ["/roll", "/roll@" + self.bot_info["username"]]):
			self.sendDice()
		else:
			self.sendMessage("I didn't quite get that, " + self.message_from_info["first_name"] + ". Please try a valid command.")
		
	def onInit(self):
		self.setMyCommands(bot_commands)
		self.getMyCommands()

newBot = Bot(hook_data)