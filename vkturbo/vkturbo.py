import aiohttp
import asyncio
import requests


class VkTurbo(object):

	API_LINK = "https://api.vk.com/method/"


	def __init__(self, access_token, version=5.85):
		self.access_token = access_token
		self.version = version


	def get_id(self, screen_name: str):
		data = {
			"v": 5.21,
			"access_token": self.access_token,
			"screen_name": screen_name
		}
		response = requests.post(f"{VkTurbo.API_LINK}utils.resolveScreenName", data=data).json()

		return response["response"]["object_id"]


	async def method(self, method_name: str, values: dict=None, raw=False):
		if "v" not in values:
			values["v"] = self.version
		if "access_token" not in values:
			values["access_token"] = self.access_token
				
		async with aiohttp.ClientSession() as session:
			response = await session.post(f"{VkTurbo.API_LINK}{method_name}", data=values)
			response = await response.json()

		return response if raw else response["response"]