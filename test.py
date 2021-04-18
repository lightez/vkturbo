from vkturbo.vkturbo import VkApi
from vkturbo.handler import EventHandler

vk = VkApi("token")
handler = EventHandler(vk)


@handler.handler
async def get_status():
	status = await vk.method("status.get", {"user_id": vk.user_id("ansqqq")})
	print(status)