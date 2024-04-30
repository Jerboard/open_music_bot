import sqlalchemy as sa
import typing as t

from datetime import date, datetime

from init import TZ
from db.base import METADATA, begin_connection


class TrackRow(t.Protocol):
    id: int
    user_id: int
    created_at: datetime
    performer: str
    title: str
    file_name: str
    mime_type: str
    file_size: int
    duration: int
    file_id: str


TrackTable = sa.Table(
    'tracks',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.now(TZ)),
    sa.Column('performer', sa.String(255)),
    sa.Column('title', sa.String(255)),
    sa.Column('file_name', sa.String(255)),
    sa.Column('mime_type', sa.String(255)),
    sa.Column('file_size', sa.Integer),
    sa.Column('duration', sa.Integer),
    sa.Column('file_id', sa.String(255)))


# добавить файл
async def add_track(
    user_id: int,
    performer: str,
    title: str,
    file_name: str,
    mime_type: str,
    file_size: int,
    duration: int,
    file_id: str
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
        file_id=file_id
    )
    async with begin_connection() as conn:
        await conn.execute(query)
