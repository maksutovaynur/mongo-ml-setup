from typing import List, Iterable

import pymongo as pm
import pymongo.results
from bson import ObjectId


class DbTable:
    def __init__(self, mongo_url: str, db_name: str, coll_name: str):
        self._client = pm.MongoClient(mongo_url)
        self._db = self._client.get_database(db_name)
        self._coll = self._db.get_collection(coll_name)

    def create_index(self, name: str, type: str = pm.TEXT, unique: bool = True):
        return self._coll.create_index([(name, type)], unique=unique)

    def insert_one(self, doc: dict) -> pm.results.InsertOneResult:
        return self._coll.insert_one(doc)

    def insert_many(self, docs: List[dict]) -> pm.results.InsertManyResult:
        return self._coll.insert_many(docs)

    def insert_by_chunks(self, docs_gen: Iterable[dict], chunk_size=100) -> pm.results.InsertManyResult:
        result = pm.results.InsertManyResult([], True)
        it = iter(docs_gen)
        done = False
        while not done:
            _chunk = []
            for _ in range(chunk_size):
                try:
                    _chunk.append(next(it))
                except StopIteration:
                    done = True
            if _chunk:
                _r = self.insert_many(_chunk)
                result.inserted_ids.extend(_r.inserted_ids)
        return result

    def find_one(self, filter: dict, projection: dict = None) -> dict:
        _prepare_filter(filter)
        return self._coll.find_one(filter, projection)

    def find_many(self, filter: dict, projection: dict = None) -> pm.cursor.Cursor:
        _prepare_filter(filter)
        return self._coll.find(filter, projection)

    def remove_many(self, filter) -> pm.results.DeleteResult:
        _prepare_filter(filter)
        return self._coll.remove(filter)

    def update_one(self, filter: dict, update: dict) -> pm.results.UpdateResult:
        _prepare_filter(filter)
        return self._coll.update_one(filter, update)

    def update_many(self, filter: dict, update: dict) -> pm.results.UpdateResult:
        _prepare_filter(filter)
        return self._coll.update_many(filter, update)

def _prepare_filter(d: dict):
    _id = d.get("_id", None)
    if _id:
        d["_id"] = ObjectId(_id)
