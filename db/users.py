import datetime
import typing as t

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_postgresql
from db.base import METADATA, begin_connection


class ProfileRow(t.Protocol):
    created_at: datetime.datetime
    last_activity: datetime.datetime
    user_id: int
    full_name: str
    username: str


ProfilesTable: sa.Table = sa.Table(
    "profiles",
    METADATA,
    sa.Column ("created_at", sa.TIMESTAMP (), nullable=False, server_default="now()"),
    sa.Column ("last_activity", sa.TIMESTAMP (), nullable=False, server_default="now()"),
    sa.Column("user_id", sa.BigInteger, primary_key=True, unique=True),
    sa.Column("full_name", sa.String, nullable=False),
    sa.Column("username", sa.String),
)


async def create_or_update_user(
        user_id: int,
        full_name: str,
        username: str
) -> None:
    now = datetime.datetime.now().replace(microsecond=0)
    payload = dict(
        user_id=user_id,
        full_name=full_name,
        username=username,
        created_at=now,
        last_activity=now
    )
    query = (
        sa_postgresql.insert(ProfilesTable)
        .values(payload)
        .on_conflict_do_update(
            index_elements=[ProfilesTable.c.user_id],
            set_={"last_activity": now,
                  "full_name": full_name,
                  "username": username,
                  }
        )
    )
    async with begin_connection() as conn:
        await conn.execute(query)