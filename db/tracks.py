import sqlalchemy as sa
import typing as t

from datetime import date, datetime

from init import TZ
from db.base import METADATA, begin_connection


class TrackRow(t.Protocol):
    id: int
    user_id: int
    created_at: datetime
    entry_type: str
    book_name: str
    performer: str
    title: str
    file_name: str
    mime_type: str
    file_size: int
    duration: int
    file_id: str
    view_count: int


TrackTable = sa.Table(
    'tracks',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.now(TZ)),
    sa.Column('entry_type', sa.String(255)),
    sa.Column('book_name', sa.String(255)),
    sa.Column('performer', sa.String(255)),
    sa.Column('title', sa.String(255)),
    sa.Column('file_name', sa.String(255)),
    sa.Column('mime_type', sa.String(255)),
    sa.Column('file_size', sa.Integer),
    sa.Column('duration', sa.Integer),
    sa.Column('file_id', sa.String(255)),
    sa.Column('view_count', sa.Integer, default=0)
)


# добавить файл
async def add_track(
        user_id: int,
        performer: str,
        title: str,
        file_name: str,
        mime_type: str,
        file_size: int,
        duration: int,
        file_id: str,
        entry_type: str = None,
        book_name: str = None

) -> None:
    added = datetime.now(TZ).replace(microsecond=0)
    query = TrackTable.insert().values(
        user_id=user_id,
        created_at=added,
        performer=performer,
        title=title,
        file_name=file_name,
        mime_type=mime_type,
        file_size=file_size,
        duration=duration,
        file_id=file_id,
        entry_type=entry_type,
        book_name=entry_type
    )
    async with begin_connection() as conn:
        await conn.execute(query)


# добавить файл
async def update_track(
        entry_id: int,
        view_count: int
) -> None:
    query = TrackTable.update().where(TrackTable.c.id == entry_id)

    if view_count:
        query = query.values(view_count=TrackTable.c.view_count + view_count)

    async with begin_connection() as conn:
        await conn.execute(query)


# добавить файл
async def get_tracks(
        user_id: int = None,
        performer: str = None,
        limit: int = None
) -> tuple[TrackRow]:
    query = TrackTable.select()

    if performer:
        query = query.where(TrackTable.c.performer == performer)
    if user_id:
        query = query.where(TrackTable.c.user_id == user_id)
    if limit:
        query = query.limit(limit=limit)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# поиск треков
async def search_tracks(request: str = '') -> tuple[TrackRow]:
    query = (TrackTable.select ().where (TrackTable.c.title.ilike (f'%{request}%')).limit(10))

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.all()


# добавить файл
async def get_track(track_id: int = None) -> TrackRow:
    query = TrackTable.select().where(TrackTable.c.id == track_id)

    async with begin_connection() as conn:
        result = await conn.execute(query)

    return result.first()
