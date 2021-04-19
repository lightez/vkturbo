from vkturbo.vkturbo import VkTurbo
from vkturbo.handler import EventHandler
from vkturbo.longpoll import LongPoll, EventType
from vkturbo.keyboard import Keyboard, KeyboardButton

vk = VkTurbo("TOKEN")
longpoll = LongPoll(vk)
handler = EventHandler()


"""
@handler.handler
async def simple_using_method():
	await vk.method("status.get", {"user_id": vk.user_id("ansqqq")})
"""

# LongPoll...
@handler.event()
async def test_keyboard():
	async for event in await longpoll.listen():
		if event[0] == 4:
			user_id = event[3]
			text = event[5].lower()

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