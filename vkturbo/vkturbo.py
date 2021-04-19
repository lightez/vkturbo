import aiohttp
import asyncio
import requests


class VkTurbo(object):

	API_LINK = "https://api.vk.com/method/"


	def __init__(self, access_token, version=5.69):
		self.access_token = access_token
		self.version = version


	def user_id(self, screen_name: str):
		data = {
			"v": self.version,
			"access_token": self.access_token,
			"screen_name": screen_name
		}
		response = requests.post(f"{VkApi.API_LINK}utils.resolveScreenName", data=data).json()

		return response["response"]["object_id"]


	async def method(self, method_name: str, values: dict=None, raw=False):
		if "v" not in values:
			values["v"] = self.version
		if "access_token" not in values:
			values["access_token"] = self.access_token
				
		async with aiohttp.ClientSession() as session:
			response = await session.post(f"{VkApi.API_LINK}{method_name}", data=values)
			response = await response.json()

		return response if raw else response["response"]