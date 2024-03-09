from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, desc, delete

from database.models import Query, Mailing
from config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)


class Database:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @staticmethod
    async def set_query(user_id: int, product_id: int):
        async with async_session() as session:
            query_instance = Query(user_id=user_id, product_id=product_id)
            session.add(query_instance)
            await session.flush()
            query_id = query_instance.id
            await session.commit()

            return query_id

    @staticmethod
    async def get_mailings(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(
                    Mailing.id, Mailing.title, Mailing.date,
                    Query.user_id, Query.product_id
                ).join(Query).where(
                    Query.user_id == user_id
                ).order_by(Mailing.id)
            )
            return result.all()

    @staticmethod
    async def get_all_mailings():
        async with async_session() as session:
            result = await session.execute(
                select(Mailing, Query.user_id, Query.product_id).join(Query)
            )
            return result.all()

    @staticmethod
    async def set_mailing(query_id: int, title: str):
        async with async_session() as session:
            mailing_instance = Mailing(title=title, query_id=query_id)
            session.add(mailing_instance)
            await session.commit()

    @staticmethod
    async def get_mailing(query_id):
        async with async_session() as session:
            result = await session.execute(
                select(Mailing).join(Query).where(
                    Query.id == query_id
                )
            )
            return result.first()

    @staticmethod
    async def delete_mailing(mailing_id: int):
        async with async_session() as session:
            await session.execute(
                delete(Mailing).where(Mailing.id == mailing_id)
            )
            await session.commit()

    @staticmethod
    async def get_queries(user_id: int, limit: int):
        async with async_session() as session:
            result = await session.execute(
                select(Query).where(Query.user_id == user_id).order_by(
                    desc(Query.date)
                ).limit(limit)
            )
            queries = result.scalars().all()

            return queries[::-1]


database = Database()
