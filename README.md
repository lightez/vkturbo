# vkturbo
Asynchronous module of vk_api

[PyPi VkTurbo](https://pypi.org/project/vkturbo/)

[Official documentation of Vk API](https://vk.com/dev/manuals)

`pip install -U vkturbo`

## Example:

```py
from vkturbo.vkturbo import VkApi
from vkturbo.handler import EventHandler

vk = VkApi("TOKEN")
handler = EventHandler(vk)


@handler.handler
async def get_user_status():
  status = await vk.method("status.get", {"user_id": vk.user_id("ansqqq")})
  print(status)
```

## LongPoll work example:

```py
from vkturbo.vkturbo import VkApi
from vkturbo.handler import EventHandler
from vkturbo.longpoll import LongPoll, EventType

vk = VkApi("token")
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

			await send_message(user_id, "Test message...")
```
