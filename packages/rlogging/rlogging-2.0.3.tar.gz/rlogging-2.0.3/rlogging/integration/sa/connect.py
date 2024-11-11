import abc
import logging

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

logger = logging.getLogger('app')


class BaseSaConnect(abc.ABC):
    engine: AsyncEngine
    session_maker: async_sessionmaker[AsyncSession]

    def __init__(self) -> None:
        self.make_engine()
        self.engine = self.make_engine()
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    @abc.abstractmethod
    def make_engine(self) -> AsyncEngine:
        pass

    async def test_connect(self) -> None:
        async with self.session_maker() as session:
            result = await session.execute(sa.text('SELECT version()'))
            logger.info('sqlalchemy connect to %s check: %s', self.engine, result.scalars().one())
