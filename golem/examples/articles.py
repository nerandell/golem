from vyked import Bus
from ..golem.golem import Golem

REGISTRY_HOST = '127.0.0.1'
REGISTRY_PORT = 4500

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

if __name__ == '__main__':
    bus = Bus()
    Article, tcp_service, http_service = Golem.generate("Article", [('username', 'id'), ('email', str)])
    tcp_service.ronin = True
    http_service.ronin = True
    bus.serve_tcp(tcp_service)
    bus.serve_http(http_service)
    bus.start(REGISTRY_HOST, REGISTRY_PORT, REDIS_HOST, REDIS_PORT)

