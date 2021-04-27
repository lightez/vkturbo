import asyncio
from vkturbo.longpoll import LongPoll, EventType
from vkturbo.vkturbo import VkTurbo


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


	def _set_attributes(self, event):
		attrs = ["user_id", "type", "from_user", "to_me", "message_id",
					"attachments", "message_data", "text", "from_chat",
					"from_group", "timestamp", "peer_id", "flags", "extra",
					"extra_values", "type_id", "vk_session"]
		attr_values = [event.user_id, event.type, event.from_user, event.to_me, event.message_id,
						event.attachments, event.message_data, event.text, event.from_chat,
						event.from_group, event.timestamp, event.peer_id, event.flags, event.extra,
						event.extra_values, event.type_id, self.vk]

		for attr, attr_value in zip(attrs, attr_values):
			setattr(Message, attr, attr_value)
	
	# test....
	def longpoll_handler(self, event_type=EventType.MESSAGE_NEW):
		def decorator(function):
			
			async def under_handler():
				async for event in await self.longpoll.listen():
					if event.type == event_type and event.to_me:
						self._set_attributes(event)

						try:
							self.tasks_handler(function(Message))
						except RuntimeError:
							continue		
							
			return self.tasks_handler(under_handler())

		return decorator
	

	def on_message(self, message_content):
		def decorator(function):

			async def under_handler():
				async for event in await self.longpoll.listen():
					if event.type == EventType.MESSAGE_NEW and event.to_me:
						self._set_attributes(event)

						if isinstance(message_content, list):
							if event.text in message_content:
								try:
									self.tasks_handler(function(Message))
								except RuntimeError:
									continue
						elif isinstance(message_content, str):
							if event.text == message_content:
								try:
									self.tasks_handler(function(Message))
								except RuntimeError:
									continue


			return self.tasks_handler(under_handler())

		return decorator


	@staticmethod
	def tasks_handler(callback):
		loop = asyncio.get_event_loop()
		task = loop.create_task(callback)

		loop.run_until_complete(task)


class Message(EventHandler):

	__slots__ = ("vk_session")


	async def send(message, keyboard=None, template=None, random_id=0):
		values = {
			"user_id": Message.user_id,
			"message": message,
			"random_id": random_id
		}

		if keyboard != None:
			values["keyboard"] = keyboard
		elif template != None:
			values["template"] = template

		await Message.vk_session.method("messages.send", values)