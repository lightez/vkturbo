# vkturbo
Asynchronous module of vk_api

[PyPi VkTurbo](https://pypi.org/project/vkturbo/)

[Official documentation of Vk API](https://vk.com/dev/manuals)

`pip install vkturbo`

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
```
