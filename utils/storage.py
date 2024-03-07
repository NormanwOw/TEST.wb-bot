from aiogram.fsm.storage.base import StorageKey

from config import storage


class Storage:

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.chat_id = user_id
        self.bot_id = 1
        self.storage = storage

    def __get_key(self) -> StorageKey:
        return StorageKey(self.bot_id, self.chat_id, self.user_id)

    async def get(self) -> dict:
        return await self.storage.get_data(self.__get_key())

    async def set(self, product_id: int, msg: str):
        await self.storage.set_data(self.__get_key(), {
            'product_id': product_id,
            'msg': msg
        })
