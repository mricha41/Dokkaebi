#formatting messages with Dokkaebi
#detailed example demonstrating
#available Telegram functionality
#when formatting messages

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
			elif command in ["/html", "/html@" + self.bot_info["username"]]:
				msg = {
					"chat_id": chat_id,
					"text": "This message uses <b>bold</b>, <i>italics</i>, <u>underline</u>, and <s>strikethrough</s> text.",
					"parse_mode": "html"
				}
				print(self.sendMessage(msg).json())
			elif command in ["/htmllink", "/htmllink@" + self.bot_info["username"]]:
				msg = {
					"chat_id": chat_id,
					"text": "here's <a href=\"https://github.com/mricha41/Dokkaebi\">a link</a> to the Dokkaebi github repo\\.",
					#"disable_web_page_preview": True,
					"parse_mode": "html"
				}
				print(self.sendMessage(msg).json())
			elif command in ["/pyhtml", "/pyhtml@" + self.bot_info["username"]]:
				msg = {
					"chat_id": chat_id,
					"text": "<code>//this is pseudo code\npseudoPrint(\"inline hello\");</code>"
							+ "<pre>pseudoPrint(\"pre-formatted hello\");</pre>"
							+ "<pre><code class=\"language-python\">\n#this is python code\ndef func(arg):\n\tdoStuff()</code></pre>",
					"parse_mode": "html"
				}
				print(self.sendMessage(msg).json())
			elif command in ["/markdown", "/markdown@" + self.bot_info["username"]]:
				msg = {
					"chat_id": chat_id,
					"text": "This message uses *bold*, _italics_, __underline__, and ~strikethrough~ text\\.",
					"parse_mode": "MarkdownV2"
				}
				print(self.sendMessage(msg).json())
			elif command in ["/markdownlink", "/markdownlink@" + self.bot_info["username"]]:
				msg = {
					"chat_id": chat_id,
					"text": "here's [a link](https://github.com/mricha41/Dokkaebi) to the Dokkaebi github repo\\.",
					#"disable_web_page_preview": True,
					"parse_mode": "MarkdownV2"
				}
				print(self.sendMessage(msg).json())
			elif command in ["/pydown", "/pydown@" + self.bot_info["username"]]:
				msg = {
					"chat_id": chat_id,
					"text": "`//this is pseudo code\npseudoPrint(\"inline hello\");`\n```\npseudoPrint(\"pre-formatted hello\");\n```\n```python\n#this is python code\ndef func(arg):\n\tdoStuff()\n```",
					"parse_mode": "MarkdownV2"
				}
				print(self.sendMessage(msg).json())
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