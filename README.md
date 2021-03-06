# vkturbo
Asynchronous module of vk api

[PyPi VkTurbo](https://pypi.org/project/vkturbo/)

[Official documentation of Vk API](https://vk.com/dev/manuals)

	pip install -U vkturbo

## Example:

```py
from vkturbo.vkturbo import VkTurbo
from vkturbo.handler import EventHandler

vk = VkTurbo("TOKEN")
handler = EventHandler(vk, longpoll=None)


@handler.handler
async def get_user_status():
  status = await vk.method("status.get", {"user_id": vk.get_id("ansqqq")})
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
		if event.type == EventType.MESSAGE_NEW: # or 4
			text = event.text.lower()
			user_id = event.user_id
			
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
							KeyboardButton().openlink("YouTube", "https://youtube.com/c/??????????")
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

## How to work with carousel?

```py
from vkturbo.vkturbo import VkTurbo
from vkturbo.handler import EventHandler
from vkturbo.longpoll import LongPoll, EventType
from vkturbo.keyboard import Keyboard, KeyboardButton, Carousel, CarouselButton

vk = VkTurbo("TOKEN")
longpoll = LongPoll(vk)
handler = EventHandler(vk, longpoll)


@handler.event()
async def test_carousel():
	async for event in await longpoll.listen():
		if event.type == EventType.MESSAGE_NEW and event.to_me:
			user_id = event.user_id
			text = event.text.lower()
			
			carousel = Carousel(
				[
					CarouselButton().openlink(
						[
							CarouselButton().element(
								title="Test title 1",
								description="Test Description 1",
								photo_id="-203980592_457239030",
								link="https://vk.com/fsoky",
								buttons=[KeyboardButton().text("button 1", "negative"), KeyboardButton().text("button 2", "primary")]
							),
							CarouselButton().element(
								title="Test title 2",
								description="Test Description 2",
								photo_id="-203980592_457239029",
								link="https://vk.com/fsoky",
								buttons=[KeyboardButton().text("button 1", "negative"), KeyboardButton().text("button 2", "primary")]
							)
						]
					)
				]
			)
			
			await vk.method("messages.send",
				{
					"user_id": user_id,
					"message": "some text...",
					"random_id": 0,
					"template": carousel.add_carousel()
				}
			)
```

![visual](https://i.imgur.com/v4C7hwe.png)

## A new variant to use LongPoll

```py
from vkturbo.vkturbo import VkTurbo
from vkturbo.handler import EventHandler, Message
from vkturbo.longpoll import LongPoll, EventType
from vkturbo.keyboard import Keyboard, KeyboardButton, Carousel, CarouselButton

vk = VkTurbo("TOKEN")
longpoll = LongPoll(vk)
handler = EventHandler(vk, longpoll)


# New LongPoll version... beta
@handler.longpoll_handler()
async def test_new_longpoll_version(message: Message):
	if message.text.lower() == "test":
		await message.send("Hello, Everyone!")
	elif message.text.lower() == "test 2":
		keyboard = Keyboard([[KeyboardButton().openlink("YouTube", "https://youtube.com/c/??????????")]])

		await message.send("Keyboard?:3", keyboard=keyboard.add_keyboard())
```

## New decorator `on_message`

```py
from vkturbo.vkturbo import VkTurbo
from vkturbo.handler import EventHandler, Message
from vkturbo.longpoll import LongPoll, EventType

vk = VkTurbo("TOKEN")
longpoll = LongPoll(vk)
handler = EventHandler(vk, longpoll)


# The bot will be answering on message, which you passed to parameters
@handler.on_message(["hello", "hi"]) # or str
async def test_on_message(message: Message):
	await message.send("Hello!")
```