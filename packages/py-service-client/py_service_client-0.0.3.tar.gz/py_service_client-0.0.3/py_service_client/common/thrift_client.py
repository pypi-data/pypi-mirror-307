import logging
import random
import time
from py_service_client.common.hooks import api_call_context


logger = logging.getLogger(__name__)

SIGNAL_CLOSE_NAME = "close"

class ThriftBaseClient(object):
    def __init__(
        self,
        host,
        port,
        transport,
        protocol,
        service,
        keepalive=None,
        pool_generation=0,
        tracking=False,
        tracker_factory=None,
        pool=None,
        socket=None,
        use_limit=None,
    ):
        self.host = host
        self.port = port
        self.transport = transport
        self.protocol = protocol
        self.service = service
        self.keepalive = keepalive
        self.alive_until = time.time() + keepalive if keepalive else None
        self.use_count = 0
        self.use_limit = use_limit
        self.pool_generation = pool_generation
        self.tracking = tracking
        self.tracker_factory = tracker_factory
        self.socket = socket
        self.pool = pool
        self.latest_use_time = time.time()

        self.client = self.get_tclient(service, protocol)
        self.init_client(self.client)

    def __repr__(self):
        return "<%s service=%s>" % (self.__class__.__name__, self.service.__name__)

    def __getattr__(self, name):
        return getattr(self.client, name)

    def init_client(self, client):
        pass

    def close(self):
        try:
            self.transport.close()
        except Exception as e:
            logger.warn("Connection close failed: %r" % e)
        finally:
            self.pool.signal_handler(SIGNAL_CLOSE_NAME, self)

    def is_expired(self):
        now = time.time()
        return (
            self.alive_until
            and now > self.alive_until
            and random.random() < (now - self.alive_until) / self.keepalive
        )

    def incr_use_count(self):
        self.use_count += 1

    def set_latest_use_time(self, time):
        self.latest_use_time = time

    def is_tired(self):
        return self.use_limit and self.use_count > self.use_limit

    def test_connection(self):
        if self.is_expired() or self.is_tired():
            return False
        try:
            self.ping()
            return True
        except:
            return False

    @classmethod
    def connect(
        cls,
        service,
        host,
        port,
        timeout=30,
        keepalive=None,
        pool_generation=0,
        tracking=False,
        tracker_factory=None,
        pool=None,
        use_limit=None,
    ):
        SOCKET = cls.get_socket_factory()(host, port)
        cls.set_timeout(SOCKET, timeout * 1000)
        PROTO_FACTORY = cls.get_protoco_factory()
        TRANS_FACTORY = cls.get_transport_factory()

        transport = TRANS_FACTORY(SOCKET)
        protocol = PROTO_FACTORY(transport)

        transport.open()

        return cls(
            host=host,
            port=port,
            transport=transport,
            protocol=protocol,
            service=service,
            keepalive=keepalive,
            pool_generation=pool_generation,
            tracking=tracking,
            tracker_factory=tracker_factory,
            pool=pool,
            socket=SOCKET,
            use_limit=use_limit,
        )

    @property
    def TTransportException(self):
        raise NotImplementedError

    @classmethod
    def get_protoco_factory(self):
        raise NotImplementedError

    @classmethod
    def get_transport_factory(self):
        raise NotImplementedError

    def get_tclient(self, service, protocol):
        raise NotImplementedError

    @classmethod
    def get_socket_factory(self):
        raise NotImplementedError

    @classmethod
    def set_timeout(cls, socket, timeout):
        raise NotImplementedError

    def set_client_timeout(self, timeout):
        self.set_timeout(self.socket, timeout)

    def get_timeout(self):
        raise NotImplementedError


class ThriftClient(ThriftBaseClient):
    def init_client(self, client):
        for api in dir(client):
            if not api.startswith(("_", "__", "send_", "recv_")):
                target = getattr(client, api)
                setattr(client, api, api_call_context(self.pool, self, api)(target))

    @property
    def TTransportException(self):
        from thrift.transport.TTransport import TTransportException

        return TTransportException

    @classmethod
    def get_protoco_factory(self):
        from thrift.protocol import TBinaryProtocol

        return TBinaryProtocol.TBinaryProtocolAccelerated

    @classmethod
    def get_transport_factory(self):
        from thrift.transport import TTransport
        return TTransport.TFramedTransport

    def get_tclient(self, service, protocol):
        if self.tracking is True:
            raise NotImplementedError(
                "%s doesn't support tracking" % self.__class__.__name__
            )
        return service.Client(protocol)

    @classmethod
    def get_socket_factory(self):
        from thrift.transport import TSocket

        return TSocket.TSocket

    @classmethod
    def set_timeout(cls, socket, timeout):
        socket.setTimeout(timeout)

    def get_timeout(self):
        return self.socket._timeout
