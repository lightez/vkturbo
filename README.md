# vkturbo
Asynchronous module of vk_api

[PyPi VkTrubo](https://pypi.org/project/vkturbo/)

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
