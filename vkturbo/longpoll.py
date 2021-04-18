import aiohttp
import asyncio


class LongPoll(object):

	def __init__(self, vk, mode=2, wait=25, group_id=None):
		self.vk = vk
		self.mode = mode
		self.wait = wait
		self.group_id = group_id

		self.key = None
		self.server = None
		self.url = None
		self.ts = None
		self.pts = mode & 2**5

		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.update_longpoll_server())


	async def update_longpoll_server(self, update_ts=True):
		values = {
			"lp_version": "3",
			"need_pts": self.pts
		}

		if self.group_id:
			values["group_id"] = self.group_id

		response = await self.vk.method("messages.getLongPollServer", values)

		self.key = response["key"]
		self.server = response["server"]
		self.ts = response["ts"]
		self.url = f"https://{response['server']}"


	async def get_event_server(self):
		values = {
			"act": "a_check",
			"key": self.key,
			"ts": self.ts,
			"server": self.server,
			"wait": self.wait,
			"mode": self.mode,
			"version": 3
		}

		async with aiohttp.ClientSession() as session:
			response = await session.get(self.url, params=values, timeout=self.wait + 10)

		if "failed" not in response:
			self.ts = response["ts"]
			if self.pts:
				self.pts = response["pts"]

			#events = [for raw_event in response["updates"]]

			# Need dorabotka blyat...