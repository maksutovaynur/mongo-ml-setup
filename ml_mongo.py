from typing import List, Iterable
import pymongo as pm
from bson import ObjectId
from pymongo.results import InsertManyResult


class DbTable:
    def __init__(self, mongo_url: str, db_name: str, coll_name: str):
        self._client = pm.MongoClient(mongo_url)
        self._db = self._client.get_database(db_name)
        self._coll = self._db.get_collection(coll_name)

    def create_index(self, name: str, type: str = pm.TEXT, unique: bool = True):
        return self._coll.create_index([(name, type)], unique=unique)

    def insert_one(self, doc: dict):
        return self._coll.insert_one(doc)

    def insert_many(self, docs: List[dict]) -> InsertManyResult:
        return self._coll.insert_many(docs)

    def insert_by_chunks(self, docs_gen: Iterable[dict], chunk_size=100) -> InsertManyResult:
        result = InsertManyResult([], True)
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

    def find_one(self, filter: dict, projection: dict = None):
        _prepare_filter(filter)
        return self._coll.find_one(filter, projection)

    def find_many(self, filter: dict, projection: dict = None):
        _prepare_filter(filter)
        return self._coll.find(filter, projection)

    def remove_many(self, filter):
        _prepare_filter(filter)
        return self._coll.remove(filter)


def _prepare_filter(d: dict):
    _id = d.get("_id", None)
    if _id:
        d["_id"] = ObjectId(_id)
