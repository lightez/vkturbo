import aiohttp
import asyncio
import json


class Keyboard(object):

	def __init__(self, button, one_time=False, inline=False):
		self.one_time = one_time
		self.inline = inline

		self.keyboard = {
			"one_time": self.one_time,
			"inline": self.inline,
			"buttons": [button]
		}

	@staticmethod
	def json_handler(*args, **kwargs):
		kwargs["ensure_ascii"] = False
		kwargs["separators"] = (",", ":")

		return json.dumps(*args, **kwargs)


	def get_keyboard(self):
		print(self.keyboard)
		return self.json_handler(self.keyboard)


	@classmethod
	def get_empty_keyboard(cls):
		keyboard = cls()
		keyboard.keyboard["buttons"] = []

		return keyboard.get_keyboard()


class KeyboardButton(object):

	def __init__(self):
		self.json_text_button =	{
			"action": {
				"type": "text",
				"label": None,
				"payload": None
			},
			"color": None
		}
		self.json_openlink_button = {
			"action": {
				"type": "open_link",
				"label": None,
				"link": None,
				"payload": None
			}
		}



	def text_button(self, label, color="secondary", payload=None):
		self.json_text_button["action"]["label"] = label
		self.json_text_button["action"]["payload"] = payload
		self.json_text_button["color"] = color

		return self.json_text_button


	def openlink_button(self, label, url, payload=None):
		self.json_openlink_button["action"]["label"] = label
		self.json_openlink_button["action"]["link"] = url
		self.json_openlink_button["action"]["payload"] = payload

		return self.json_openlink_button