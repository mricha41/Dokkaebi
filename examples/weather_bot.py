#weather bot example

#if you don't whish to set this
#just copy the file to the top-level
#folder and run it there w/out this
import sys
sys.path.append("../dokkaebi")
print(sys.path)

import string
import datetime

import requests
from dokkaebi import dokkaebi
from configparser import ConfigParser

#appending to sys.path allows
#config to be read relative to that path
#even though this file is in the examples folder
config = ConfigParser()
config.read('weather_bot.ini')

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
		{'command': 'start', 'description': 'starts the bot.', 'example': "Just issue /start in the Telegram message box."},
		{'command': 'cityweather', 'description': 'Get the current weather information of any US city.', 'example': "\nThe command: /cityweather San Diego will return weather information for San Diego."},
	]
}

#you'll need your own API key
#at api.openweathermap.org
openweather = {
	'key': config["OpenWeather"]["API_KEY"]
}

class Bot(dokkaebi.Dokkaebi):
	def handleData(self, data):
		print(data)
		command = None
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
				weather = "https://external-content.duckduckgo.com/iu/?u=https://media.giphy.com/media/5yvoGUhBsuBwY/giphy.gif&f=1&nofb=1"
				print(self.sendAnimation({"chat_id": chat_id, "animation": weather}).json())
				msg = {
					"chat_id": chat_id,
					"text": "Thanks for using "  + self.bot_info["username"] + ", " + user_first_name + "!\n" + "It's always wise to check the weather before you run outside. " + "&#128514;",
					"parse_mode": "html"
				}
				print(self.sendMessage(msg).json())
				print(self.sendMessage({
					"chat_id": chat_id, 
					"text": "Just submit a command to get weather information.\nFor example, the command: /cityweather San Diego\nwill return weather information for San Diego.\nUse the /help command for the full list of commands."
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
				print(self.sendMessage(msg).json())
			elif command in ["/cityweather", "/cityweather@" + self.bot_info["username"]]:
				#check how long the city name is
				#and act accordingly
				if len(user_parameters) > 1:
					city = " ".join(user_parameters)
					city = city.translate(str.maketrans('', '', string.punctuation))
					city = city.replace("’", "")
				elif len(user_parameters) == 0:
					city = None				
				else:
					city = user_parameters[0]
					city = city.translate(str.maketrans('', '', string.punctuation))
					city = city.replace("’", "")

				#print(city)

				if city != None:
					#openweather provides units parameter - we use imperial in the US
					#but the other option is metric, or don't pass in units and you'll get
					#a temperature in kelvin. if you do that, you can use the conversion
					#functions if/when you wish to convert (for example the user wants to see it
					#differently and you require units as a command parameter)
					res = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=imperial&appid=" + openweather["key"]).json()
					#print(res)
					temp = None
					min_temp = None
					max_temp = None
					feel = None
					pressure = None
					humidity = None
					main = None
					desc = None
					icon = None
					name = None
					country = None
					sunrise = None
					sunset = None

					if res.get("main") and res["main"] != None:
						temp = res["main"]["temp"]
						feel = res["main"]["feels_like"]
						min_temp = res["main"]["temp_min"]
						max_temp = res["main"]["temp_max"]
						pressure = res["main"]["pressure"]
						humidity = res["main"]["humidity"]

					if res.get("weather") and res["weather"][0] != None:
						main = res["weather"][0]["main"]
						desc = res["weather"][0]["description"]
						icon = res["weather"][0]["icon"]

					if res.get("sys") and res["sys"] != None:
						country = res["sys"]["country"]
						sunrise = date = datetime.datetime.fromtimestamp(res["sys"]["sunrise"])
						sunset = datetime.datetime.fromtimestamp(res["sys"]["sunset"])

					if res.get("name") and res["name"] != None:
						name = res["name"]

					if temp and feel and min_temp and max_temp and pressure and humidity and main and desc and icon and name and country and sunrise and sunset:
						#don't just stand there...
						#send them the weather!
						print(self.sendPhoto({
							"chat_id": chat_id,
							"photo": "http://openweathermap.org/img/wn/" + icon + "@2x.png", 
							"caption": "The current weather for " + name + ", " + country + ":" +
									"\n--------------------------------" +
									"\n" + main + "/" + desc + "\n<b>Temperature</b>: {}".format(temp) +
									"\n<i>Feels like</i>: {}".format(feel) +
									"\n<b>Low</b>: {}".format(min_temp) + "\n<b>High</b>: {}".format(max_temp) +
									"\n--------------------------------" +
									"\n<i>Pressure</i>: {}".format(pressure) + "\n<i>Humidity</i>: {}".format(humidity) +
									"\n--------------------------------" +
									"\n<i>Sunrise</i>: {}".format(sunrise.ctime()) + "\n<i>Sunset</i>: {}".format(sunset.ctime()),
							"parse_mode": "html"
						}).json())
					else:
						print(self.sendMessage({
							"chat_id": chat_id, 
							"text": "There was an error with the city you entered. Please check the spelling and try again."
						}).json())
				else:
					print(self.sendMessage({
						"chat_id": chat_id, 
						"text": "There was an error with the city you entered. Please check the spelling and try again."
					}).json())
			else:
				msg = {
					"chat_id": chat_id,
					"text": "I didn't quite get that, " + user_first_name + ". Please try a valid command."
				}
				print(self.sendMessage(msg).json())

	def kelvinToFahrenheit(self, temp):
		return (temp - 273.15) * 1.8000 + 32.00

	def kelvinToCelsius(self, temp):
		return temp - 273.15
		
	def onInit(self):
		print(self.setMyCommands(bot_commands).json())
		print(self.getMyCommands().json())

newBot = Bot(hook_data)