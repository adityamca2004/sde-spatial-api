from typing import Any, Optional
import datetime
from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, Index, Integer, PrimaryKeyConstraint, String, Table, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import NullType

class Base(DeclarativeBase):
    pass


class IndiaOutline(Base):
    __tablename__ = 'India_Outline'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='India_Outline_pkey'),
        Index('sidx_India_Outline_geom', 'geom', postgresql_using='gist')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    geom: Mapped[Optional[Any]] = mapped_column(Geometry('GEOMETRY'))
    STATE: Mapped[Optional[str]] = mapped_column(String(50))


class ApiImportedData(Base):
    __tablename__ = 'api_imported_data'
    __table_args__ = (
        PrimaryKeyConstraint('external_id', name='api_imported_data_pkey'),
    )

    external_id: Mapped[str] = mapped_column(Text, primary_key=True)
    imported_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    srid: Mapped[Optional[int]] = mapped_column(BigInteger)
    srtext: Mapped[Optional[str]] = mapped_column(Text)
    auth_name: Mapped[Optional[str]] = mapped_column(Text)
    auth_srid: Mapped[Optional[int]] = mapped_column(BigInteger)
    proj4text: Mapped[Optional[str]] = mapped_column(Text)


class Books(Base):
    __tablename__ = 'books'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='books_pkey'),
        Index('ix_books_id', 'id'),
        Index('ix_books_title', 'title')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[Optional[str]] = mapped_column(String)
    author: Mapped[Optional[str]] = mapped_column(String)


t_geography_columns = Table(
    'geography_columns', Base.metadata,
    Column('f_table_catalog', String),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geography_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', Text)
)


t_geometry_columns = Table(
    'geometry_columns', Base.metadata,
    Column('f_table_catalog', String(256, 'C')),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geometry_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', String(30))
)


class SpatialRefSys(Base):
    __tablename__ = 'spatial_ref_sys'
    __table_args__ = (
        CheckConstraint('srid > 0 AND srid <= 998999', name='spatial_ref_sys_srid_check'),
        PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )

    srid: Mapped[int] = mapped_column(Integer, primary_key=True)
    auth_name: Mapped[Optional[str]] = mapped_column(String(256))
    auth_srid: Mapped[Optional[int]] = mapped_column(Integer)
    srtext: Mapped[Optional[str]] = mapped_column(String(2048))
    proj4text: Mapped[Optional[str]] = mapped_column(String(2048))
# Create an engine connected to the environment database

