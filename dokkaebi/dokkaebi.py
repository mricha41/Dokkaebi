import json
import requests
import cherrypy

class Dokkaebi(object):
	"""
	Dokkaebi is a class for easily creating
	Telegram bots and interacting with users.
	
	Data Members:
	self.bot_info - json data with information about your bot from the Telegram API.
	self.webhook_config - user-supplied dictionary with hook information (see __init__).
	self.webhook_info - json data with information about your webhook from the Telegram API.
	self.update_received_count - number of updates received counted since the bot was instantiated.

	self.message_info - json data with information about the current message received from a Telegram update.
	self.chat_info - json data with information about the current chat received from a Telegram update.
	self.message_from_info - json data with information about the user the Telegram update provides inside the message.
	self.message_date - json data with the current message's date.
	self.message_text - json data with the current message's text.
	"""

	def __init__(self, hook):
		"""
		Dokkaebi bot construction requires passing in a dictionary of the following form, for example:
		hook = {
			'hostname': '127.0.0.1', 
			'port': 80, 
			'token': 'yourtelegrambottokenhere', 
			'url': 'https://yourwebhookurlhere.com'
		}
		d = dokkaebi.Dokkaebi(hook)
		PRECONDITION:
		None
		POSTCONDITION:
		Dokkaebi class is constructed from the given dictionary values.
		"""
		self.webhook_config = hook
		self.update_received_count = 0

		print("Starting Dokkaebi bot...")
		print("Ctrl+C to quit")

		#make sure there is no live webhook before setting it
		self.deleteWebhook()

		#store current webhook info upon setting it successfully
		self.setWebhook()
		self.webhook_info = self.getWebhookInfo()

		#store the bot info
		self.bot_info = self.getMe()

		#hook for init work that
		#needs accomplished in derived classes
		#before the server starts
		self.onInit()

		#crank up a CherryPy server
		cherrypy.config.update({
		    'environment': 'production',
		    'log.screen': False,
		    'server.socket_host': self.webhook_config["hostname"],
		    'server.socket_port': self.webhook_config["port"],
		})
		cherrypy.quickstart(self, '/')

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def index(self):
		"""
		Handles all of the update logic for the Dokkaebi bot.
		Because this varies wildy depending on the application,
		simply calling a user-defined function was the easiest
		way of handling the issue. The caller must inherit from
		Dokkaebi and override the handleData(data) function to
		implement their own update logic:

		class Bot(dokkaebi.Dokkaebi):
			#overridden function...
			def handleData(data):
				print("do some stuff with the update data...")

		This enables the user to hook into the CherryPy server
		listening at the webhook base url and customize the
		update logic.

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		Requests are received on the assigned port at the webhook url provided.
		Additionally, processing of the updates is passed on to self.handleData(data)
		which is implemented in the user-defined override outside of this class.
		"""
		data = cherrypy.request.json

		#store some for the convenience of calling
		#methods such as sendMessage(...) without
		#user having to mess with housekeeping data
		self.message_info = data["message"]
		self.chat_info = data["message"]["chat"]
		self.message_from_info = data["message"]["from"]
		self.message_date = data["message"]["date"]
		self.message_text = data["message"]["text"]
		
		#callback to a user-defined function
		#for handling updates
		self.handleData(data)

	def onInit(self):
		"""
		Override this method to hook into the constructor and
		handle tasks that need to be handled upon construction
		of the Dokkaebi class.
		"""

	def handleData(self, data):
		"""
		Override this method to hook into the update method and
		handle json data retrieved from Telegram webhook request
		"""

	def setWebhook(self, hook = None):
		"""
		Sets the Telegram Bot webhook, defaults to using the current hook information
		stored in Dokkaebi or by passing in a dictionary in the form:
		{"url": "https://yourwebhookurl.com"}

		RETURNS: boolean

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance may or may not have been constructed.

		POSTCONDITION:
		self.webhook_config["url"] is set, the request is made, and one of the following takes place:
			* request status code 200 received and True is returned indicating the request was successful and
			  the webhook is set on Telegram
			* request status code returned indicates one of the following types of errors:
				* internal server error
				* client error
				* request object returned
		See the Telegram Bot API documentation for more information about what
		status codes may be returned when a request is made to /setWebhook.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/setWebhook'
		if(hook == None):
			r = requests.post(url, data = {"url": self.webhook_config["url"]})
		else:
			self.webhook_config["url"] = hook["url"]
			r = requests.post(url, data = {"url": self.webhook_config["url"]})

		if(r.status_code == 200):
			print("Webhook set: " + self.webhook_config["url"])
		else:
			print("error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

		return r

	def getWebhookInfo(self):
		"""
		Retrieves and returns the current webhook info stored
		in the Dokkaebi bot.

		RETURNS: WebhookInfo json object
		
		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance may or may not have been constructed.
		Dokkaebi bot may have had webhook data assigned on construction.
		
		POSTCONDITION:
		Dokkaebi sends the request to get the webhook information from Telegram. Upon success,
		a json object is printed to the console and the WebhookInfo json object is
		returned to the caller In the event of an error,
		the request object is returned after error is printed to the console. Also, see the
		Telegram Bot API documentation for what types of status codes to expect
		when making a request to /getWebhookInfo.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/getWebhookInfo'
		r = requests.get(url)
		if(r.status_code == 200):
			print("Webhook info:")
			print(r.json())
			return r.json()["result"]
		else:
			print("Webhook info could not be retrieved - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)
				return r

	def deleteWebhook(self):
		"""
		Deletes the current webhook on Telegram and resets the internal webhook data
		stored in the Dokkaebi bot.

		RETURNS: boolean
		
		PRECONDITION:
		Dokkaebi bot must have webhook data assigned via the constructor. A Telegram
		webhook may or may not have been previously set. (see Telegram Bot API for /setWebhook,
		/getWebhookInfo, and /deleteWebhook)
		
		POSTCONDITION:
		Dokkaebi sends the request to get remove the webhook from Telegram and the internal
		Dokkaebi bot webhook data is reset to None. Upon success, the HTTP status code
		is printed to the console and the request returns True. Upon error, the status code is printed to the console
		along with the whole request object returned. (see Python requests documentation for more 
		information on what status codes could be returned from requests.post(...)). Also, see the
		Telegram Bot API documentation for what types of status codes to expect
		when making a request to /deleteWebhook.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/deleteWebhook'
		r = requests.post(url)
		if(r.status_code == 200):
			print("Webhook deleted...")
		else:
			print("Webhook could not be deleted - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

		return r

	def getMe(self):
		"""
		Retrieves the current information about your bot from the Telegram API.
		
		RETURNS: User json object

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.
		
		POSTCONDITION:
		If the request succeeds, a User json object with the bot info will be returned.
		Otherwise, the request failed with an error and the request object is printed
		to the console and returned. Also, see the Telegram Bot API documentation for 
		what types of status codes to expect when making a request to /getMe.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/getMe'
		r = requests.get(url)
		if(r.status_code == 200):
			print("Bot information:")
			print(r.json())
			return r.json()["result"]
		else:
			print("Bot information could not be retrieved - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)
				return r

	def sendMessage(self, message_data):
		"""
		Sends a message to Telegram.
		The message_data parameter should be a dictionary of the following form:
		{ 
			"chat_id": YOURCHATID, #required - string or integer according to Telegram API docs
			"text": "YOUR MESSAGE", #required - the message text you want to send.
			"parse_mode": None, #optional - string for html or markdown if desired (See Telegram API documentation).
			"disable_web_page_preview": None, #optional - boolean disables a web preview if sending a link.
			"disable_notification": None, #optional - boolean disables notification sound and sends message silently.
			"reply_to_message_id": None, #optional - optional id of the original message if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: Message json object

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the message and the Message json object is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendMessage'
		r = requests.post(url, data = message_data)

		if(r.status_code == 200):
			print("Message sent...")
		else:
			print("Message could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)
		
		return r

	def forwardMessage(self, message_data):
		"""
		Forward a message to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs.
			"from_chat_id": FROMCHATID, #required - string or integer for the chat where the original message is from.
			"message_id": MESSAGEID, #required - integer id of the message being forwarded.
			"disable_notification": None, #optional - disable notification sound to send photo to user silently.
		}

		RETURNS: sent Message json object

		PRECONDITION:
		A Telegram bot has been created, the Dokkaebi instance has been constructed, and a
		message exists to forward.

		POSTCONDITION:
		On success, Telegram receives the forwarded message and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/forwardMessage'
		r = requests.post(url, data = message_data)

		if(r.status_code == 200):
			print("Message sent...")
		else:
			print("Message could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

		return r

	def sendPhoto(self, photo_data):
		"""
		Send a photo to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs
			"photo": FILEORURL, #required - input file, file_id as string or url to photo as string (see Telegram API doc).
			"caption": "CAPTION", #optional - description of the photo.
			"parse_mode": None, #optional - html or markdown (see Telegram API doc).
			"disable_notification": None, #optional - disable notification sound to send photo to user silently.
			"reply_to_message_id": None, #optional - optional id of the original message if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: sent Message json object

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the photo request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendPhoto'
		r = requests.post(url, data = photo_data)

		if(r.status_code == 200):
			print("Photo sent...")
		else:
			print("Photo could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

		return r

	def sendAudio(self, audio_data):
		"""
		Send audio to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs
			"audio": FILEORURL, #required - input file, file_id as string or url to audio file as string (see Telegram API doc).
			"caption": "CAPTION", #optional - string description of the audio.
			"parse_mode": None, #optional - string html or markdown (see Telegram API doc).
			"duration": None, #optional - int duration in seconds.
			"performer": None, #optional - string performer name.
			"title": None, #optional - string title of audio.
			"thumb": None, #optional - input file or string (see Telegram API doc) 
			"disable_notification": None, #optional - disable notification sound to send audio to user silently.
			"reply_to_message_id": None, #optional - optional id of the original message if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: sent Message json object

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the audio request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendAudio'
		r = requests.post(url, data = audio_data)

		if(r.status_code == 200):
			print("Audio sent...")
		else:
			print("Audio could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

		return r

	def sendDocument(self, document_data):
		"""
		Send a document to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs
			"document": FILEORURL, #required - input file, file_id as string or url to document as string (see Telegram API doc).
			"thumb": None, #optional - input file or string (see Telegram API doc)
			"caption": "CAPTION", #optional - string description of the document.
			"parse_mode": None, #optional - string html or markdown (see Telegram API doc).
			"disable_notification": None, #optional - disable notification sound to send document to user silently.
			"reply_to_message_id": None, #optional - optional id of the original message if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: sent Message json object

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the document request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendDocument'
		r = requests.post(url, data = document_data)

		if(r.status_code == 200):
			print("Document sent...")
		else:
			print("Document could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

		return r

	def sendVideo(self, video_data):
		"""
		Send a video to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs
			"video": FILEORURL, #required - input file, file_id as string or url to video file as string (see Telegram API doc).
			"duration": None, #optional - int duration in seconds.
			"width": None, #optional - int width of video.
			"height": None, #optional - int height of video.
			"thumb": None, #optional - input file or string (see Telegram API doc)
			"caption": "CAPTION", #optional - string description of the video.
			"parse_mode": None, #optional - string html or markdown for video caption (see Telegram API doc).
			"supports_streaming": None, #optional - True if video can be streamed.			 
			"disable_notification": None, #optional - disable notification sound to send video to user silently.
			"reply_to_message_id": None, #optional - optional id of the original message if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: sent Message json object
		
		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the video request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendVideo'
		r = requests.post(url, data = video_data)

		if(r.status_code == 200):
			print("Video sent...")
		else:
			print("Video could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

		return r
	
	def sendAnimation(self, animation_data):
		"""
		Send an animation to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs.
			"animation": "FILE", #required - InputFile or string according to Telegram API docs.
			"duration": None, #optional - int duration in seconds.
			"width": None, #optional - int width of animation.
			"height": None, #optional - int height of animation.
			"thumb": None, #optional - input file or string (see Telegram API doc).
			"caption": "CAPTION", #optional - string description of the animation.
			"parse_mode": None, #optional - string html or markdown for animation caption (see Telegram API doc).
			"disable_notification": None, #optional - disable notification sound to send animation to user silently.
			"reply_to_message_id": None, #optional - optional id of the original message if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: sent Message json object

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the animation request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendAnimation'
		r = requests.post(url, data = animation_data)

		if(r.status_code == 200):
			print("Animation sent...")
		else:
			print("Animation could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

	def sendVoice(self, voice_data):
		"""
		Send a voice message to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs.
			"voice": "FILE", #required - InputFile or string according to Telegram API docs.
			"caption": "CAPTION", #optional - string description of the voice.
			"parse_mode": None, #optional - string html or markdown for voice caption (see Telegram API doc).
			"duration": None, #optional - int duration in seconds.
			"disable_notification": None, #optional - disable notification sound to send voice to user silently.
			"reply_to_message_id": None, #optional - optional id of the original message if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: sent Message json object
		
		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the voice request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendVoice'
		r = requests.post(url, data = voice_data)

		if(r.status_code == 200):
			print("Voice sent...")
		else:
			print("Voice could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

	def sendVideoNote(self, video_note_data):
		"""
		Send a video note to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs.
			"video_note": "FILE", #required - InputFile or string according to Telegram API docs.
			"duration": None, #optional - int duration in seconds.
			"length": None, #optional - int diameter of video note according to Telegram API docs.
			"thumb": None, #optional - input file or string (see Telegram API doc)
			"disable_notification": None, #optional - disable notification sound to send video note to user silently.
			"reply_to_message_id": None, #optional - optional id of the original message if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: sent Message json object
		
		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the video note request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendVideoNote'
		r = requests.post(url, data = video_note_data)

		if(r.status_code == 200):
			print("Video note sent...")
		else:
			print("Video note could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

	def sendMediaGroup(self, media_group_data):
		"""
		Send a group of photos or videos as an album to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs.
			"media": [
				{"type": "photo", "media": "URLTOPHOTO"},
				{"type": "photo", "media": "URLTOPHOTO"},
				...
			, # required - json-serialized array of InputMediaPhoto or InputMediaVideo (2-10 items).
			"disable_notification": None, #optional - disable notification sound to send media group to user silently.
			"reply_to_message_id": None #optional - optional id of the original message if the message is a reply.
		}

		RETURNS: array of sent Message json object
		
		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the media group request and the array of Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendMediaGroup'
		r = requests.post(url, json = media_group_data)

		if(r.status_code == 200):
			print("Media group sent...")
		else:
			print("Media group could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

	def sendLocation(self, location_data):
		"""
		Send a location to Telegram.
		{
			"chat_id": CHATID, #required - string or integer according to Telegram API docs.
			"latitude": LAT, #required - float latitude of location.
			"longitude": LONG, #required - float longitude of location.
			"live_period": , #optional - period in seconds for which the location will be updated (60-86400 seconds).
			"disable_notification": None, #optional - disable notification sound to send location to user silently.
			"reply_to_message_id": None, #optional - optional id of the original message if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}
		
		RETURNS: sent Message json object
		
		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the location request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendLocation'
		r = requests.post(url, data = location_data)

		if(r.status_code == 200):
			print("Location sent...")
		else:
			print("Location could not be sent - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)

	def editMessageLiveLocation(self):
		"""
		Edit a live location message.
		{
			"chat_id": CHATID, #optional - string or integer according to Telegram API docs. (required if inline_message_id is not specified)
			"message_id": MESSAGEID, #optional - integer id of the live location message being edited. (required if inline_message_id is not specified)
			"inline_message_id": MESSAGEID, # optional - integer id of inline message (required if chat_id and message_id are not specified)
			"latitude": LAT, #required - float latitude of location.
			"longitude": LONG, #required - float longitude of location.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: if bot owned the message a sent Message json object is returned, otherwise True is returned
		
		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the edit live location request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""

	def stopMessageLiveLocation(self):
		"""
		Stop a live location message.
		{
			"chat_id": CHATID, #optional - string or integer according to Telegram API docs. (required if inline_message_id is not specified)
			"message_id": MESSAGEID, #optional - integer id of the live location message being edited. (required if inline_message_id is not specified)
			"inline_message_id": MESSAGEID, # optional - integer id of inline message (required if chat_id and message_id are not specified)
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply.
		}

		RETURNS: if bot owned the message a sent Message json object is returned, otherwise True is returned
		
		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		On success, Telegram receives the stop live location request and the Message json object
		is returned. 
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""

	def sendVenue(self):
		"""
		Send a venue to Telegram.
		{
	
		}

		RETURNS: sent Message json object
		
		PRECONDITION:

		POSTCONDITION:
		"""
	def sendContact(self):
		"""
		Send a contact to Telegram.
		{
	
		}

		RETURNS: sent Message json object
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def sendPoll(self):
		"""
		Send a poll to Telegram.
		{
	
		}

		RETURNS: sent Message json object
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def sendDice(self, dice_data = None):
		"""
		Send dice to the Telegram user.
		Does not require parameters because Dokkaebi
		keeps track of the chat id internally and sends
		the dice to the corresponding chat automatically.
		Dokkaebi keeps track of the current chat id internally, but
		it can also be overridden at your option.
		Override the default dice_data parameter to a dictionary of the following form
		(only chat_id parameter is required):
		{ 
			"chat_id": YOURCHATID, #required - string or integer according to Telegram API docs.
			"emoji": None, #optional - accepts a string with unicode value or copy/paste literal emoji (probably works).
			"disable_notification": None, #optional - boolean disables notification sound and sends dice silently.
			"reply_to_message_id": None, #optional - integer optional message id if the message is a reply.
			"reply_markup": None #optional - See Telegram API documentation, pass in InlineKeyboardMarkup or ReplyKeyboardMarkup or ReplyKeyboardRemove or ForceReply
		}

		RETURNS: sent Message json object

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.

		POSTCONDITION:
		The dice have been sent to the Telegram user and the request object is returned
		to the caller to process at their option.
		Otherwise, if the request failed with an error the request object is printed
		to the console and returned.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/sendDice'
		if dice_data is not None:
			r = requests.post(url, data = dice_data)
		else:
			r = requests.post(url, data = {"chat_id": self.chat_info["id"]})

		if(r.status_code == 200):
			print("Dice sent...")
		else:
			print("Dice could not be set - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)
		
		return r

	def sendChatAction(self):
		"""
		Send a chat action (indication that something is happening on the bot side) to Telegram.
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def getUserProfilePhotos(self):
		"""
		Get a list of profile photos from a Telegram user.
		{
	
		}

		RETURNS: UserProfilePhotos json object
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def getFile(self):
		"""
		Get information about a file and prepare it for downloading (see Telegram API doc).
		{
	
		}

		RETURNS: File json object
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def kickChatMember(self):
		"""
		Remove a Telegram user from a chat (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def unbanChatMember(self):
		"""
		Unban a previously kicked Telegram user from a chat (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def restrictChatMember(self):
		"""
		Restrict a Telegram user (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def promoteChatMember(self):
		"""
		Promote or demote a Telegram user in a chat (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def setChatAdministratorCustomTitle(self):
		"""
		Set a custom title for an administrator in a chat promoted by the bot (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def setChatPermissions(self):
		"""
		Set default chat permissions for a chat (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def exportChatInviteLink(self):
		"""
		Generate a new invite link for a chat (see Telegram API doc).
		{
	
		}

		RETURNS: new link as a string
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def setChatPhoto(self):
		"""
		Set the profile photo for the chat - does not work for private chats (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def deleteChatPhoto(self):
		"""
		Delete the profile photo for the chat - does not work for private chats (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def setChatTitle(self):
		"""
		Set the title of the chat - does not work for private chats (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def setChatDescription(self):
		"""
		Set the description of the chat - bot must be an administrator (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def pinChatMessage(self):
		"""
		Pin a message in a chat - bot must be an administrator (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def unpinChatMessage(self):
		"""
		Unpin a message in a chat - bot must be an administrator (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def leaveChat(self):
		"""
		Make bot leave a chat (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def getChat(self):
		"""
		Get information about a chat - returns a Chat json object (see Telegram API doc).
		{
	
		}

		RETURNS: Chat json object
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def getChatAdministrators(self):
		"""
		Get a list of administrators in a chat (see Telegram API doc).
		{
	
		}

		RETURNS: array of ChatMember json object
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def getChatMembersCount(self):
		"""
		Get the number of members in a chat (see Telegram API doc).
		{
	
		}

		RETURNS: integer
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def getChatMember(self):
		"""
		Get information about a chat member (see Telegram API doc).
		{
	
		}

		RETURNS: ChatMember json object
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def setChatStickerSet(self):
		"""
		Set a new group sticker set in a chat - bot must be an administrator (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def deleteChatStickerSet(self):
		"""
		Remove group sticker set from a chat - bot must be an administrator (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def answerCallbackQuery(self):
		"""
		Send answers to callback queries sent from inline keyboards (see Telegram API doc).
		{
	
		}

		RETURNS: boolean
		
		PRECONDITION:

		POSTCONDITION:
		"""

	def setMyCommands(self, commands):
		"""
		Sets the command list for your bot programatically
		rather than through the Bot Father. Accepts an array
		of dictionary with the following form (up to 100 commands):

		#sets the list to empty:
		self.setMyCommands({"commands": []})
		commands = {
			"commands": [
				{"command": "COMMAND TEXT HERE", "description": "DESCRIPTION HERE"},
				{"command": "COMMAND TEXT HERE", "description": "DESCRIPTION HERE"},
				...
			]
		}

		RETURNS: boolean

		#sets the list with valid commands:
		self.setMyCommands(commands)

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed. 
		Either no list or a previous list of commands may exist.
		
		POSTCONDITION:
		If the request succeeds, the bot command list will be overwritten on Telegram and
		a request object returned to the caller for optional processing.
		If the request fails, Telegram should revert to the existing list or the default
		list if a list was never supplied to the Bot Father. Otherwise, if the request 
		failed with an error the request object is printed to the console and returned to the caller.
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/setMyCommands'
		r = requests.post(url, json = commands)
		if(r.status_code == 200):
			print("Commands set...")
		else:
			print("Commands could not be set - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)
		
		return r

	def getMyCommands(self):
		"""
		Gets the current command list for your bot programatically
		rather than through the Bot Father. Returns a json object
		from the Telegram API.

		RETURNS: array of BotCommand json object

		PRECONDITION:
		A Telegram bot has been created and the Dokkaebi instance has been constructed.
		
		POSTCONDITION:
		The current command list will be returned as JSON if the
		request succeeds. Otherwise, if the request failed with an error 
		the request object is printed to the console and returned to the caller. 
		"""
		url = 'https://api.telegram.org/bot' + self.webhook_config["token"] + '/getMyCommands'
		r = requests.get(url)
		if(r.status_code == 200):
			print("Command list:")
			print(r.json())
			return r.json()
		else:
			print("Commands could not be retrieved - error: " + format(r.status_code))
			if r and r is not None:
				print("Request object returned: \n" + r.text)
				return r

	def closeServer(self):
		"""
		STUB
		"""
		print("Server closed...")
		
		return