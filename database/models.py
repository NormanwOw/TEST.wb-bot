from datetime import datetime

from sqlalchemy import BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Query(Base):
    __tablename__ = 'queries'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow
    )
    mailing = relationship('Mailing')


class Mailing(Base):
    __tablename__ = 'mailings'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow
    )
    query_id: Mapped[int] = mapped_column(
        ForeignKey('queries.id', ondelete='CASCADE'), nullable=False
    )
