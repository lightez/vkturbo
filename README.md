# vkturbo
Asynchronous module of vk api

[PyPi VkTurbo](https://pypi.org/project/vkturbo/)

[Official documentation of Vk API](https://vk.com/dev/manuals)

`pip install -U vkturbo`

## Example:

```py
from vkturbo.vkturbo import VkTurbo
from vkturbo.handler import EventHandler

vk = VkTurbo("TOKEN")
handler = EventHandler(vk, longpoll=None)


@handler.handler
async def get_user_status():
  status = await vk.method("status.get", {"user_id": vk.user_id("ansqqq")})
  print(status)
```

## LongPoll work example:

```py
from vkturbo.vkturbo import VkTurbo
from vkturbo.handler import EventHandler
from vkturbo.longpoll import LongPoll, EventType

vk = VkTurbo("token")
longpoll = LongPoll(vk)
handler = EventHandler(vk, longpoll)

# Simple function for sending a messages
async def send_message(user_id, message):
	await vk.method("messages.send", {
		"user_id": user_id,
		"message": message,
		"random_id": 0
	})


@handler.event()
async def new_lonpoll_version_vkturbo():
	async for event in await longpoll.listen():
		if event[0] == EventType.MESSAGE_NEW: # or 4
			text = event[5].lower()
			user_id = event[3]
			
			if text == "test":
				await send_message(user_id, "Test message...")
```

## Work with keyboard

```py
from vkturbo.vkturbo import VkTurbo
from vkturbo.handler import EventHandler
from vkturbo.longpoll import LongPoll, EventType
from vkturbo.keyboard import Keyboard, KeyboardButton

vk = VkTurbo("TOKEN")
longpoll = LongPoll(vk)
handler = EventHandler(vk, longpoll)


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
```

![visual](https://i.imgur.com/PMn5Lso.png)
