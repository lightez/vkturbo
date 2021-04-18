from vkturbo.vkturbo import VkApi
from vkturbo.handler import EventHandler
from vkturbo.longpoll import LongPoll, EventType

vk = VkApi("token")
handler = EventHandler(vk)


@handler.handler
async def get_status():
	status = await vk.method("status.get", {"user_id": vk.user_id("ansqqq")})
	print(status)


@handler.event()
async def test_longpoll():
	async for event in await LongPoll(vk).listen():
		if event[0] == EventType.MESSAGE_NEW: # or 4
			msg = event[5]
			user_id = event[3]

			if msg == "test":
				await vk.method("messages.send",
					{
						"user_id": user_id,
						"message": "test message",
						"random_id": 0
					}
				)

	# There bug... ;3