from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, desc, delete

from database.models import Query, Mailing
from config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine)


class Database:

    @staticmethod
    async def set_query(user_id: int, product_id: int):
        async with async_session() as session:
            query_instance = Query(user_id=user_id, product_id=product_id)
            session.add(query_instance)
            await session.commit()

    @staticmethod
    async def get_queries(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Query).where(Query.user_id == user_id).order_by(
                    desc(Query.date)
                ).limit(5)
            )
            queries = result.scalars().all()

            return queries[::-1]

    @staticmethod
    async def add_mailing(user_id: int, msg: str, product_id: int):
        async with async_session() as session:
            mailing_instance = Mailing(
                user_id=user_id, message=msg, product_id=product_id
            )
            session.add(mailing_instance)
            await session.commit()

    @staticmethod
    async def get_mailings(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Mailing).where(Mailing.user_id == user_id).order_by(Mailing.id)
            )
            return result.scalars().all()

    @staticmethod
    async def get_mailing(user_id: int, product_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Mailing).where(
                    Mailing.user_id == user_id, Mailing.product_id == product_id
                )
            )
            return result.scalars().first()

    @staticmethod
    async def delete_mailing(user_id: int, mailing_id: int):
        async with async_session() as session:
            await session.execute(
                delete(Mailing).where(Mailing.user_id == user_id, Mailing.id == mailing_id)
            )
            await session.commit()

    @staticmethod
    async def get_all_mailings():
        async with async_session() as session:
            result = await session.execute(
                select(Mailing)
            )
            return result.scalars().all()


database = Database()
