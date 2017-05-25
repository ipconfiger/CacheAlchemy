# coding=utf8
from unittest import TestCase

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, String
import redis

engine = create_engine("postgresql+psycopg2://fiveddd@localhost/cache_test", convert_unicode=True, echo=True)
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

    def test_cached_dummy_backend_cache(self):
        from CacheAlchemy import cached_by_id, init_cached
        from CacheAlchemy import DummyBackend
        init_cached(db, DummyBackend())

        testtable = cached_by_id(TestTable, 1)
        testtable1 = cached_by_id(TestTable, 1)

        testtable1.name = "thygasdad"
        print testtable1.name
        db.flush()
        db.commit()
        testtable3 = cached_by_id(TestTable, 1)
        self.assertTrue(True)

    def test_cached_redis_backend_by_id(self):
        from CacheAlchemy import cached_by_id, init_cached
        from CacheAlchemy import RedisBackend
        init_cached(db, RedisBackend(redis.Redis(host='127.0.0.1', port=6379, db=1)))

        table = cached_by_id(TestTable, 2)
        table.name = "qqqq"
        db.flush()
        db.commit()
        table1 = cached_by_id(TestTable, 2)
        table1.name = 'pppppppppppp'
        db.commit()
        self.assertTrue(True)

    def test_cached_redis_backend_by_filter(self):
        from CacheAlchemy import cached_by_condition, init_cached
        from CacheAlchemy import RedisBackend
        init_cached(db, RedisBackend(redis.Redis(host='127.0.0.1', port=6379, db=1)))

        table = cached_by_condition(TestTable, TestTable.id == 2)
        table.name = "aaaa"
        db.flush()
        db.commit()
        table1 = cached_by_condition(TestTable, TestTable.id == 2)
        table1.name = 'bbbbb'
        db.commit()
        self.assertTrue(True)
