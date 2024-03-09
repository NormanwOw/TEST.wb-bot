import aiohttp

from database.models import Mailing, Query
from database.orm import database
import messages


class WBService:

    @staticmethod
    def __get_product_url(product_id: int) -> str:
        return f'https://card.wb.ru/cards/v1/detail?appType=1&curr=' \
               f'rub&dest=-1257786&spp=30&nm={product_id}'

    async def __get_product_data(self, product_id: int) -> dict:
        async with aiohttp.ClientSession() as session:
            url = self.__get_product_url(product_id)
            async with session.get(url) as resp:
                response = await resp.json()
                return response

    async def get_product(self, product_id: int) -> tuple:
        data = await self.__get_product_data(product_id)

        products = data['data']['products']
        msg = ''
        title = ''
        for product in products:
            title = product.get('name')
            rating = product.get('reviewRating')

            msg += f'🛍 <u><b>{title}</b></u>\n\n' \
                   f'🆔 {product_id}\n' \
                   f'⭐️ {rating}\n' \

            for size in product['sizes']:
                size_name = size.get('name')
                if size_name:
                    msg += f'======================\n'
                    price = size.get('salePriceU') / 100
                    msg += f'Размер: {size_name}\n' \
                           f'Цена: 💶 {price}0₽\n'
                else:
                    price = product.get('salePriceU') / 100
                    msg += f'Цена: 💶 {price}0₽\n'

                qty = 0
                for wh in size['stocks']:
                    qty += wh.get('qty')
                msg += f'Количество: {qty}\n'

        return msg, title


class Response:

    @staticmethod
    async def get_queries_msg(user_id: int) -> str:
        queries = await database.get_queries(user_id, 5)

        if queries:
            msg = '<b>Последние 5 запросов</b>\n\n'
            for query in queries:
                date, time = query.date.strftime('%d.%m.%Y %H:%M:%S').split()
                msg += f'🆔 {query.product_id}\n' \
                       f'📆 {date} ⏱ {time}\n' \
                       f'=======================\n'
        else:
            msg = messages.EMPTY_QUERIES_MSG

        return msg

    @staticmethod
    async def get_mailing_msg(mailing: Mailing | Query) -> str:
        date, time = mailing.date.strftime('%d.%m.%Y %H:%M:%S').split()
        msg = f'🛍 <u><b>{mailing.title}</b></u>\n\n' \
              f'🆔 {mailing.product_id}\n' \
              f'📆 {date} ⏱ {time}\n'

        return msg


