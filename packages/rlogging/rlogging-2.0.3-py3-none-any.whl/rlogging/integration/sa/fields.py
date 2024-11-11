from datetime import datetime
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy.orm import (
    Mapped,  # noqa: F401
    mapped_column,
)

int_32_pk_inc_identity = sa.Identity(
    start=1,
    increment=1,
    minvalue=1,
    maxvalue=2**31 - 1,
    cycle=False,
    cache=1,
)

int_64_pk_inc_identity = sa.Identity(
    start=1,
    increment=1,
    minvalue=1,
    maxvalue=2**63 - 1,
    cycle=False,
    cache=1,
)


int_32_inc_pk = Annotated[
    int,
    mapped_column(
        sa.Integer,
        primary_key=True,
        server_default=int_32_pk_inc_identity,
    ),
]

int_64_inc_pk = Annotated[
    int,
    mapped_column(
        sa.BigInteger,
        primary_key=True,
        server_default=int_64_pk_inc_identity,
    ),
]


int_32_pk = Annotated[int, mapped_column(sa.Integer, primary_key=True)]
int_64_pk = Annotated[int, mapped_column(sa.BigInteger, primary_key=True)]

slug_unique = Annotated[str, mapped_column(sa.String(64), nullable=False, unique=True)]

int_32 = Annotated[int, mapped_column(sa.SmallInteger())]
int_64 = Annotated[int, mapped_column(sa.BigInteger())]

text = Annotated[str, mapped_column(sa.Text())]

str_1 = Annotated[str, mapped_column(sa.String(1))]
str_2 = Annotated[str, mapped_column(sa.String(2))]
str_8 = Annotated[str, mapped_column(sa.String(8))]
str_16 = Annotated[str, mapped_column(sa.String(16))]
str_32 = Annotated[str, mapped_column(sa.String(32))]
str_64 = Annotated[str, mapped_column(sa.String(64))]
str_128 = Annotated[str, mapped_column(sa.String(128))]
str_256 = Annotated[str, mapped_column(sa.String(256))]

timestamp = Annotated[datetime, mapped_column(sa.DateTime)]
created_at = Annotated[datetime, mapped_column(sa.DateTime, server_default=sa.func.now())]
updated_at = Annotated[datetime, mapped_column(sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())]


flag_false = Annotated[bool, mapped_column(sa.Boolean, default=False, nullable=False)]
flag_true = Annotated[bool, mapped_column(sa.Boolean, default=True, nullable=False)]
