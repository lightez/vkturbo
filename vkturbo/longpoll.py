import aiohttp
import asyncio
from enum import IntEnum


class LongPollMode(IntEnum):
	#: Получать вложения
	GET_ATTACHMENTS = 2

	#: Возвращать расширенный набор событий
	GET_EXTENDED = 2**3

	#: возвращать pts для метода `messages.getLongPollHistory`
	GET_PTS = 2**5

	#: В событии с кодом 8 (друг стал онлайн) возвращать
	#: дополнительные данные в поле `extra`
	GET_EXTRA_ONLINE = 2**6

	#: Возвращать поле `random_id`
	GET_RANDOM_ID = 2**7


DEFAULT_MODE = sum(LongPollMode)


class EventType:
	#: Замена флагов сообщения (FLAGS:=$flags)
	MESSAGE_FLAGS_REPLACE = 1

	#: Установка флагов сообщения (FLAGS|=$mask)
	MESSAGE_FLAGS_SET = 2

	#: Сброс флагов сообщения (FLAGS&=~$mask)
	MESSAGE_FLAGS_RESET = 3

	#: Добавление нового сообщения.
	MESSAGE_NEW = 4

	#: Редактирование сообщения.
	MESSAGE_EDIT = 5

	#: Прочтение всех входящих сообщений в $peer_id,
	#: пришедших до сообщения с $local_id.
	READ_ALL_INCOMING_MESSAGES = 6

	#: Прочтение всех исходящих сообщений в $peer_id,
	#: пришедших до сообщения с $local_id.
	READ_ALL_OUTGOING_MESSAGES = 7

	#: Друг $user_id стал онлайн. $extra не равен 0, если в mode был передан флаг 64.
	#: В младшем байте числа extra лежит идентификатор платформы
	#: (см. :class:`VkPlatform`).
	#: $timestamp — время последнего действия пользователя $user_id на сайте.
	USER_ONLINE = 8

	#: Друг $user_id стал оффлайн ($flags равен 0, если пользователь покинул сайт и 1,
	#: если оффлайн по таймауту). $timestamp — время последнего действия пользователя
	#: $user_id на сайте.
	USER_OFFLINE = 9

	#: Сброс флагов диалога $peer_id.
	#: Соответствует операции (PEER_FLAGS &= ~$flags).
	#: Только для диалогов сообществ.
	PEER_FLAGS_RESET = 10

	#: Замена флагов диалога $peer_id.
	#: Соответствует операции (PEER_FLAGS:= $flags).
	#: Только для диалогов сообществ.
	PEER_FLAGS_REPLACE = 11

	#: Установка флагов диалога $peer_id.
	#: Соответствует операции (PEER_FLAGS|= $flags).
	#: Только для диалогов сообществ.
	PEER_FLAGS_SET = 12

	#: Удаление всех сообщений в диалоге $peer_id с идентификаторами вплоть до $local_id.
	PEER_DELETE_ALL = 13

	#: Восстановление недавно удаленных сообщений в диалоге $peer_id с
	#: идентификаторами вплоть до $local_id.
	PEER_RESTORE_ALL = 14

	#: Один из параметров (состав, тема) беседы $chat_id были изменены.
	#: $self — 1 или 0 (вызваны ли изменения самим пользователем).
	CHAT_EDIT = 51

	#: Изменение информации чата $peer_id с типом $type_id
	#: $info — дополнительная информация об изменениях
	CHAT_UPDATE = 52

	#: Пользователь $user_id набирает текст в диалоге.
	#: Событие приходит раз в ~5 секунд при наборе текста. $flags = 1.
	USER_TYPING = 61

	#: Пользователь $user_id набирает текст в беседе $chat_id.
	USER_TYPING_IN_CHAT = 62

	#: Пользователь $user_id записывает голосовое сообщение в диалоге/беседе $peer_id
	USER_RECORDING_VOICE = 64

	#: Пользователь $user_id совершил звонок с идентификатором $call_id.
	USER_CALL = 70

	#: Счетчик в левом меню стал равен $count.
	MESSAGES_COUNTER_UPDATE = 80

	#: Изменились настройки оповещений.
	#: $peer_id — идентификатор чата/собеседника,
	#: $sound — 1/0, включены/выключены звуковые оповещения,
	#: $disabled_until — выключение оповещений на необходимый срок.
	NOTIFICATION_SETTINGS_UPDATE = 114


class LongPoll(object):

	def __init__(self, vk, mode=DEFAULT_MODE, wait=25, group_id=None):
		self.vk = vk
		self.mode = mode.value if isinstance(mode, LongPollMode) else mode
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

		if update_ts:
			self.ts = response["ts"]


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
			response = await response.json()
		
		if "failed" not in response:
			self.ts = response["ts"]
			events = [raw_event for raw_event in response["updates"]]

			return events
		elif response["failed"] == 1:
			self.ts = response["ts"]
		elif response["failed"] == 2:
			self.update_longpoll_server(update_ts=False)
		elif response["failed"] == 3:
			self.update_longpoll_server()

		return []


	@asyncio.coroutine
	async def listen(self):
		while True:
			for event in await self.get_event_server():
				yield event