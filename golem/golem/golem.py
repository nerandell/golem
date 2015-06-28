from asyncio import coroutine
import logging
from .base_type import BaseType
from vyked.sql import PostgresStore
from vyked.utils.log import log
from vyked.services import TCPApplicationService, HTTPApplicationService

IDENTIFIER = 'identifier'
CREATED = 'created'


class _Store(PostgresStore):
    _logger = logging.getLogger(__name__)

    def __init__(self, entity):
        self._table_name = entity.__name__

    @log(logger=_logger)
    @coroutine
    def insert_ele(self, entity: BaseType):
        yield from self.insert(self._table_name, dict(vars(entity)))

    @log(logger=_logger)
    @coroutine
    def update_ele(self, entity: BaseType):
        yield from self.update(self._table_name, values=dict(vars(entity)),
                               where_keys=[{IDENTIFIER: ('=', getattr(entity, entity.id))}])

    @log(logger=_logger)
    @coroutine
    def get_ele(self, id):
        return (yield from self.select(self._table_name, order_by=CREATED, where_keys=[{IDENTIFIER: ('=', id)}]))

    @log(logger=_logger)
    @coroutine
    def delete_ele(self, id):
        yield from self.delete(self._table_name, where_keys=[{IDENTIFIER: ('=', id)}])


class _Service:
    _logger = logging.getLogger(__name__)

    def __init__(self, store):
        self._store = store

    @log(logger=_logger)
    @coroutine
    def insert_ele(self, entity: BaseType):
        pass

    @log(logger=_logger)
    @coroutine
    def update_ele(self, entity: BaseType):
        pass

    @log(logger=_logger)
    @coroutine
    def get_ele(self, id):
        pass

    @log(logger=_logger)
    @coroutine
    def delete_ele(self, id):
        pass

class _TCPService(TCPApplicationService, _Service):
    def __init__(self, store):
        self._store = store
        super(_TCPService, self).__init__('FakeService', 1, '127.0.0.1', 4501)


class _HTTPService(HTTPApplicationService):
    def __init__(self, store):
        self._store = store
        super(_HTTPService, self).__init__('FakeService', 1, '127.0.0.1', 4502)


class Golem:
    def __init__(self):
        pass

    @classmethod
    def generate(cls, entity, fields):
        element = Golem.generate_class(entity, fields)
        store = cls._get_store(element)
        return element, _TCPService(store), _HTTPService(store)

    @classmethod
    def generate_class(cls, name, fields):
        return type(name, (BaseType,), {'_fields': fields + BaseType._fields})

    @staticmethod
    def _get_store(entity: BaseType.__class__):
        return _Store(entity)
