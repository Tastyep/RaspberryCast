""" Abstraction of a repository """

from tinydb import where

from OpenCast.infra import Id

from .context import Context
from .error import RepoError


class Repository:
    def __init__(self, database, schema):
        self._db = database
        self._schema = schema
        self._collection = database.table(type(schema).__name__)

    def create(self, entity):
        if self.exists(entity.id):
            raise RepoError(f"cannot create: '{entity}' already exists")

        self._collection.insert(entity.to_dict())

    def update(self, entity):
        e = self.get(entity.id)
        if e is None:
            raise RepoError(f"cannot update: '{entity}' doesn't exist")

        self._collection.update(entity.to_dict(), where("id") == str(entity.id))

    def delete(self, entity):
        self._collection.remove(where("id") == str(entity.id))

    def list(self, ids=None):
        results = (
            self._collection.all()
            if ids is None
            else self._collection.search(lambda model: Id(model["id"]) in ids)
        )
        return [self._schema.load(result) for result in results]

    def get(self, id_):
        results = self._collection.search(where("id") == str(id_))
        return None if not results else self._schema.load(results[0])

    def exists(self, id_):
        return self.get(id_) is not None

    def make_context(self):
        return Context(self)