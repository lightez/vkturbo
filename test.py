from vkturbo.vkturbo import VkTurbo
from vkturbo.handler import EventHandler
from vkturbo.longpoll import LongPoll, EventType
from vkturbo.keyboard import Keyboard, KeyboardButton

vk = VkTurbo("TOKEN")
longpoll = LongPoll(vk)
handler = EventHandler(vk, longpoll) # If you wanna use just methods: longpoll=None


"""
@handler.handler
async def simple_using_method():
	await vk.method("status.get", {"user_id": vk.get_id("ansqqq")})
"""

# LongPoll...
@handler.event()
async def test_keyboard():
	async for event in await longpoll.listen():
		if event.type == EventType.MESSAGE_NEW:
			user_id = event.user_id
			text = event.text.lower()

			if text == "test":
				keyboard = Keyboard(
					[
						[
							KeyboardButton().text("Primary", "primary"),
							KeyboardButton().text("Secondary", "secondary"),
							KeyboardButton().text("Positive", "positive")
						],
						[
							KeyboardButton().text("Negative", "negative"),
							KeyboardButton().openlink("YouTube", "https://youtube.com/c/Фсоки")
						],
						[
							KeyboardButton().location()
						]
					]
				)

				await vk.method("messages.send",
					{
						"user_id": user_id,
						"message": "something text...",
						"keyboard": keyboard.add_keyboard(),
						"random_id": 0
					}
				)