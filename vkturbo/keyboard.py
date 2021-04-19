import aiohttp
import asyncio
import json


class Keyboard(object):

	def __init__(self, button: list, one_time=False, inline=False):
		self.one_time = one_time
		self.inline = inline

		self.keyboard = {
			"one_time": self.one_time,
			"inline": self.inline,
			"buttons": button
		}


	def add_keyboard(self):
		return json.dumps(self.keyboard, ensure_ascii=False)


class KeyboardButton(object):

	def text(self, label, color, payload=None):
		return {
			"action": {
				"type": "text",
				"label": label,
				"payload": payload
			},
			"color": color
		}


	def openlink(self, label, link, payload=None):
		return {
			"action": {
				"type": "open_link",
				"label": label,
				"link": link,
				"payload": payload
			}
		}


	def location(self, payload=None):
		return {
			"action": {
				"type": "location",
				"payload": payload
			}
		}


	def vkpay(self, pay_hash, payload=None):
		return {
			"action": {
				"type": "vkpay",
				"hash": pay_hash,
				"payload": payload
			}
		}


	def vkapps(self, app_id, owner_id, label, app_hash, payload=None):
		return {
			"action": {
				"type": "vkapps",
				"app_id": app_id,
				"owner_id": owner_id,
				"label": label,
				"hash": app_hash,
				"payload": payload
			}
		}