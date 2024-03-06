from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, desc

from database.models import Query
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


database = Database()
