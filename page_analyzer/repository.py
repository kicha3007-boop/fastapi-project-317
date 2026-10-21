from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from page_analyzer.models import Url, UrlCheck


async def get_urls_with_last_check(
    session: AsyncSession,
) -> list[tuple[Url, UrlCheck | None]]:
    last_check_ids = (
        select(
            UrlCheck.url_id,
            func.max(UrlCheck.id).label("check_id"),
        )
        .group_by(UrlCheck.url_id)
        .subquery()
    )
    statement = (
        select(Url, UrlCheck)
        .outerjoin(last_check_ids, last_check_ids.c.url_id == Url.id)
        .outerjoin(UrlCheck, UrlCheck.id == last_check_ids.c.check_id)
        .order_by(Url.id.desc())
    )
    return list((await session.exec(statement)).all())


async def find_url_by_name(session: AsyncSession, name: str) -> Url | None:
    statement = select(Url).where(Url.name == name)
    return (await session.exec(statement)).first()


async def get_url(session: AsyncSession, url_id: int) -> Url | None:
    return await session.get(Url, url_id)


async def save(session: AsyncSession, record: Url | UrlCheck) -> None:
    session.add(record)
    await session.commit()
    await session.refresh(record)
