import aiohttp

from database.orm import database


class WBService:

    @staticmethod
    def __get_product_url(product_id: int) -> str:
        return f'https://card.wb.ru/cards/v1/detail?appType=1&curr=' \
               f'rub&dest=-1257786&spp=30&nm={product_id}'

    async def __get_product(self, product_id: int) -> dict:
        async with aiohttp.ClientSession() as session:
            url = self.__get_product_url(product_id)
            async with session.get(url) as resp:
                response = await resp.json()
                return response

    async def get_product_msg(self, product_id: int) -> str:
        data = await self.__get_product(product_id)

        products = data['data']['products']
        msg = ''
        for product in products:
            product_name = product.get('name')
            rating = product.get('reviewRating')

            msg += f'🛍 {product_name}\n' \
                   f'🆔: {product_id}\n' \
                   f'⭐️{rating}\n' \

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
        return msg


class Response:

    @staticmethod
    async def get_queries_msg(user_id: int) -> str:
        queries = await database.get_queries(user_id)

        if queries:
            msg = 'Последние 5 запросов\n\n'
            for query in queries:
                date, time = query.date.strftime('%d.%m.%Y %H:%M:%S').split()
                msg += f'[id:{query.id}] | артикул: {query.product_id}\n' \
                       f'📆{date} ⏱{time}\n' \
                       f'=======================\n'
        else:
            msg = 'Список запросов пуст'

        return msg



