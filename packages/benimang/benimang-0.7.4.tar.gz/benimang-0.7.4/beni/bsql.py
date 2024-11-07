from __future__ import annotations

import logging
import re
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Sequence, Type, TypeVar, cast

import aiomysql
from pydantic import BaseModel

from .bfunc import getSqlPlacement, toAny
from .btype import Null


class BModel(BaseModel):

    _tableName: str = ''

    @classmethod
    def tableName(cls):
        if type(cls._tableName) is not str:
            className = cls.__name__
            result = [className[0].lower()]
            for char in className[1:]:
                if char.isupper():
                    result.extend(['_', char.lower()])
                else:
                    result.append(char)
            cls._tableName = ''.join(result)
        return cls._tableName


_BModel = TypeVar('_BModel', bound=BModel)
_T = TypeVar('_T')


_sqlFormatRe = re.compile(r'\s*\n\s*')


def _sqlFormat(sql: str, args: Sequence[Any]) -> str:
    sql = _sqlFormatRe.sub(' ', sql).strip()
    if '%x' in sql:
        sql = sql.replace('%x', makePlacement(args))
    return sql


def makePlacement(value: int | Sequence[Any] | set[Any]) -> str:
    if type(value) is int:
        return ', '.join(['%s'] * value)
    else:
        num = len(toAny(value))
        return ', '.join(['%s'] * num)


class MysqlDbCursor:

    def __init__(self, cursor: aiomysql.Cursor):
        self.cursor = cursor

    @property
    def connection(self) -> aiomysql.Connection:
        return toAny(self.cursor.connection)

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    @property
    def rowcount(self):
        return self.cursor.rowcount

    async def commit(self):
        await self.connection.commit()

    async def rollback(self):
        await self.connection.rollback()

    async def execute(self, sql: str, *args: Any):
        sql = _sqlFormat(sql, args)
        return await self.cursor.execute(sql, args)

    async def getTupleOne(self, sql: str, *args: Any) -> tuple[Any, ...] | None:
        '获取单行数据，以 tuple 形式返回'
        sql = _sqlFormat(sql, args)
        await self.cursor.execute(sql, args)
        result = cast(tuple[Any], await self.cursor.fetchone())
        return result or None

    async def getDictOne(self, sql: str, *args: Any) -> dict[str, Any] | None:
        '获取单行数据，以 dict 形式返回'
        result = await self.getTupleOne(sql, *args)
        if result:
            columns = self._getColumns()
            result = {v: result[i] for i, v in enumerate(columns)}
            return result
        return None

    async def getOne(self, modelClass: Type[_BModel], sql: str, *args: Any) -> _BModel | None:
        '获取单行数据，以 modelClass 实例返回'
        data = await self.getDictOne(sql, *args)
        if data:
            return modelClass(**data)
        return None

    async def getTupleList(self, sql: str, *args: Any) -> tuple[tuple[Any, ...]]:
        '获取多行数据，以 tuple 形式返回'
        sql = _sqlFormat(sql, args)
        await self.cursor.execute(sql, args)
        result = cast(tuple[tuple[Any]], await self.cursor.fetchall())
        return result or []

    async def getDictList(self, sql: str, *args: Any) -> list[dict[str, Any]]:
        '获取多行数据，以 dict 形式返回'
        result = await self.getTupleList(sql, *args)
        if result:
            columns = self._getColumns()
            return [{v: row[i] for i, v in enumerate(columns)} for row in result]
        return []

    async def getList(self, modelClass: Type[_BModel], sql: str, *args: Any) -> list[_BModel]:
        '获取多行数据，以 modelClass 实例返回'
        result = await self.getDictList(sql, *args)
        return [modelClass(**x) for x in result]

    async def getValue(self, valueClass: Type[_T], sql: str, *args: Any) -> _T | None:
        '获取单个值'
        sql = _sqlFormat(sql, args)
        await self.cursor.execute(sql, args)
        result: Sequence[Any] = await self.cursor.fetchone()
        return result[0] if result else None

    async def getValueList(self, valueClass: Type[_T], sql: str, *args: Any) -> list[_T] | None:
        '获取多个值'
        sql = _sqlFormat(sql, args)
        await self.cursor.execute(sql, args)
        result: Sequence[Sequence[Any]] = await self.cursor.fetchall()
        return [x[0] for x in result] if result else []

    async def addOne(self, model: BModel, *, tableName: str = '') -> Any:
        columns: list[str] = []
        values: list[Any] = []
        for k, v in model.model_dump(exclude_unset=True).items():
            columns.append(f'`{k}`')
            values.append(v)
        tableName = tableName or model.__class__.tableName()
        sql = f'''INSERT INTO `{tableName}` ( {','.join(columns)} ) VALUES %s'''
        await self.cursor.execute(sql, [values])
        return self.lastrowid

    async def saveOne(self, model: BModel, *, tableName: str = ''):
        columns: list[str] = []
        values: list[Any] = []
        for k, v in model.model_dump(exclude_unset=True).items():
            columns.append(f'`{k}`')
            values.append(v)
        tableName = tableName or model.__class__.tableName()
        updateSql = ','.join([f'{x} = VALUES( {x} )' for x in columns])
        sql = f'''INSERT INTO `{tableName}` ( {','.join(columns)} ) VALUES %s ON DUPLICATE KEY UPDATE {updateSql}'''
        return await self.cursor.execute(sql, [values])

    async def saveList(self, modelList: Sequence[BModel], *, tableName: str = ''):
        assert modelList, 'modelList 必须至少有一个元素'
        columns: list[str] = []
        values: list[Sequence[Any]] = []
        for k in modelList[0].model_dump().keys():
            columns.append(f'`{k}`')
        for model in modelList:
            values.append(tuple(model.model_dump().values()))
        tableName = tableName or modelList[0].__class__.tableName()
        updateSql = ','.join([f'{x} = VALUES( {x} )' for x in columns])
        sql = f'''INSERT INTO `{tableName}` ( {','.join(columns)} ) VALUES {getSqlPlacement(columns, '%s')} ON DUPLICATE KEY UPDATE {updateSql}'''
        return await self.cursor.executemany(sql, values)

    def _getColumns(self) -> tuple[str, ...]:
        return tuple(x[0] for x in toAny(self.cursor.description))


@dataclass
class MysqlDb:
    host: str
    port: int
    user: str
    password: str
    db: str = ''
    _pool: aiomysql.Pool = Null

    @asynccontextmanager
    async def getCursor(self, isAutoRollback: bool = True) -> AsyncGenerator[MysqlDbCursor, None]:
        isEcho = logging.getLogger().level is logging.DEBUG
        if not self._pool:
            self._pool = await aiomysql.create_pool(  # type: ignore
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db or None,
                echo=isEcho,
            )
        async with cast(aiomysql.Connection, self._pool.acquire()) as connection:
            async with cast(aiomysql.Cursor, connection.cursor()) as cursor:
                try:
                    yield MysqlDbCursor(cursor)
                finally:
                    if isAutoRollback:
                        await connection.rollback()

    async def close(self):
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()

    def makeByDb(self, db: str):
        return MysqlDb(self.host, self.port, self.user, self.password, db=db)


class ConditionMaker:

    _statement = ''

    def __init__(self):
        self._ary: list[str] = []
        self._args: list[Any] = []

    def add(self, sql: str, *args: Any):
        self._ary.append(sql)
        self._args.extend(args)

    @property
    def args(self) -> list[Any]:
        return self._args

    def __str__(self) -> str:
        if self._ary:
            return f'{self._statement} ' + ' AND '.join([f'({x})' for x in self._ary])
        else:
            return ''


class WhereMaker(ConditionMaker):
    _statement = 'WHERE'


class HavingMaker(ConditionMaker):
    _statement = 'HAVING'


class OnMaker(ConditionMaker):
    _statement = 'ON'
