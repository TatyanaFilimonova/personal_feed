import os
import json
from dataclasses import dataclass
from functools import lru_cache
import aiofiles
import asyncio

from personal_feed.settings import ABSOLUTE_DB_PATH

from abc import ABCMeta, abstractmethod


class UserDoesntExists(Exception):
    pass


@dataclass
class User:
    user_id: str
    name: str
    user_type: str
    city: str


class AbstractDBFile(metaclass=ABCMeta):

    def __init__(self, file_path):
        self._file_path = file_path
        self._loaded = False
        self.content = dict()

    async def _load_db(self):
        is_load = await self._get_json()
        self._loaded = True
        return is_load

    def get_user(self, _id) -> User:
        try:
            # we have str id in json
            raw_user = self.content[str(_id)]
        except KeyError:
            raise UserDoesntExists(f'User id {_id} doesn\'t exists')
        return User(
            user_id=_id,
            name=raw_user['name'],
            user_type=raw_user['type'],
            city=raw_user['city'],
        )


class SyncJsonDataBase(AbstractDBFile):

    async def _get_json(self):
        async with aiofiles.open(self._file_path, mode='r') as f:
            contents = await f.read()
            self.content = json.loads(contents) 
            return True;
           

@lru_cache(maxsize=1)
def get_db_sync():
    db = SyncJsonDataBase(ABSOLUTE_DB_PATH)
    print(type(db))    
    print(db._file_path)
    return db


async def get_user_sync(user_id):
    db: SyncJsonDataBase = get_db_sync()
    await db._load_db()
    return db.get_user(user_id)
