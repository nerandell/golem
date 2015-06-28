from vyked import Bus
from ..golem.golem import Automator
from ..golem.types import Type

REGISTRY_HOST = '127.0.0.1'
REGISTRY_PORT = 4500

class Article(Type):

    _fields = Type._fields + [('username', 'id'), ('email', str)]

    def __init__(self, username, email):
        self.username = username
        self.email = email
        super(Article, self).__init__()

if __name__ == '__main__':
    bus = Bus()
    tcp_service, http_service = Automator.generate("Article", {'username': str, })
    tcp_service.ronin = True
    http_service.ronin = True
    bus.serve_tcp(tcp_service)
    bus.serve_http(http_service)
    bus.start(REGISTRY_HOST, REGISTRY_PORT)
