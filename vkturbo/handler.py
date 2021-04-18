import asyncio


class EventHandler:

	def __init__(self, vk, longpoll):
		self.vk = vk
		self.longpoll = longpoll


	@staticmethod
	def handler(function):
		loop = asyncio.get_event_loop()
		loop.run_until_complete(function())


	def event(self, message=None, attachments=None):
		def decorator(callback):
			self.tasks_wrapper(callback)

			return callback

		return decorator


	@staticmethod
	def tasks_wrapper(callback):
		loop = asyncio.get_event_loop()
		task = loop.create_task(callback())

		loop.run_until_complete(task)

	# Нужно доработать.....;3