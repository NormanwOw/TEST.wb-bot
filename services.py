import datetime

import aiohttp

from database.orm import database


class WBService:

    @staticmethod
    def __get_product_url(product_id: int) -> str:
        return f'https://card.wb.ru/cards/v1/detail?appType=1&curr=' \
               f'rub&dest=-1257786&spp=30&nm={product_id}'

    async def get_product(self, user_id: int, product_id: int) -> dict:
        async with aiohttp.ClientSession() as session:
            url = self.__get_product_url(product_id)
            async with session.get(url) as resp:
                response = await resp.json()
                await database.set_query(user_id, product_id)
                return response


class Response:

    async def get_queries_msg(self, user_id: int) -> str:
        msg = 'Последние 5 запросов\n\n'

        queries = await database.get_queries(user_id)
        if queries:
            for query in queries:
                date, time = query.date.strftime('%d.%m.%Y %H:%M:%S').split()
                msg += f'[id:{query.id}] | артикул: {query.product_id}\n' \
                       f'📆{date} ⏱{time}\n' \
                       f'=======================\n'

        return msg



