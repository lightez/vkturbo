import asyncio

class EventHandler:

	def __init__(self, vk):
		self.vk = vk

	@staticmethod
	def handler(function):
		loop = asyncio.get_event_loop()
		loop.run_until_complete(function())