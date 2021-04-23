import asyncio
from aiovk.longpoll import LongPoll, EventType, Message
from aiovk.vkturbo import VkTurbo


class EventHandler:

	def __init__(self, vk, longpoll):
		self.vk = vk
		self.longpoll = longpoll


	@staticmethod
	def handler(function):
		loop = asyncio.get_event_loop()
		loop.run_until_complete(function())


	def event(self):
		def decorator(callback):
			self.tasks_handler(callback())

			return callback

		return decorator

	
	# test....
	def longpoll_handler(self, event_type=EventType.MESSAGE_NEW):
		def decorator(function):
			self.tasks_handler(function(Message))
			
			async def under_handler():
				async for event in await self.longpoll.listen():
					print(event)

			return self.tasks_handler(under_handler())

		return decorator
		

	@staticmethod
	def tasks_handler(callback):
		loop = asyncio.get_event_loop()
		task = loop.create_task(callback)

		loop.run_until_complete(task)