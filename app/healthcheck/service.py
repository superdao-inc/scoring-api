import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class HealthCheckService:
    session: async_sessionmaker[AsyncSession]

    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session = session

    async def _get_from_db(self) -> str:
        async with self.session() as session:
            v = await session.execute(sa.text("SELECT 1"))
            return str(v.scalar())

    async def health(self) -> dict[str, str]:
        p = await self._get_from_db()
        return {'status': 'ok', 'db': 'ok' if p else 'fail'}
