# coding=utf8
from unittest import TestCase

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, String

engine = create_engine("postgresql+psycopg2://liming:@localhost/cache_test", convert_unicode=True, echo=True)
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine,
                                 ))

class DeclaredBase(object):
    pass

Base = declarative_base(cls=DeclaredBase)
Base.query = db.query_property()

class TestTable(Base):
    __tablename__ = "testtable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))


class TestCached(TestCase):
    def test_cached (self):
        from CacheAlchemy import cached, init_cached
        from CacheAlchemy import DummyBackend
        init_cached(db, DummyBackend())

        testtable = cached(TestTable, 1)
        testtable1 = cached(TestTable, 1)

        testtable1.name = "thygasdad"
        print testtable1.name
        db.flush()
        db.commit()
        testtable3 = cached(TestTable, 1)
        self.assertTrue(True)

