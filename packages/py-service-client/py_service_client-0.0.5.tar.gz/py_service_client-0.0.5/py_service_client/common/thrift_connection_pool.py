import logging
import contextlib
import socket
from py_service_client.common.thrift_client import ThriftClient, ThriftBaseClient
from collections import deque
from py_service_client.common.hooks import client_get_hook


logger = logging.getLogger(__name__)

SIGNAL_CLOSE_NAME = "close"


def validate_host_port(host, port):
    if not all((host, port)):
        raise RuntimeError("host and port not valid: %r:%r" % (host, port))


class BaseThriftConnnection(object):
    QueueCls = deque

    def __init__(
        self,
        service,
        timeout=30,
        name=None,
        raise_empty=False,
        max_conn=30,
        connection_class=ThriftClient,
        keepalive=None,
        tracking=False,
        tracker_factory=None,
        use_limit=None,
    ):
        if service is None:
            raise RuntimeError("Service cannot be None")

        self.service = service
        self.timeout = timeout
        self.name = name or service.__name__
        self.connections = self.QueueCls()
        self.raise_empty = raise_empty
        self.max_conn = max_conn
        self.connection_class = connection_class
        self.keepalive = keepalive
        self.use_limit = use_limit
        self.generation = 0
        self.tracking = tracking
        self.tracker_factory = tracker_factory
        self.conn_close_callbacks = []
        self.__api_method_cache = {}

    @contextlib.contextmanager
    def annotate(self, **kwds):
        if not self.tracking:
            raise NotImplementedError("Tracking is not enabled")

        with self.tracker_factory.annotate(**kwds) as annotation:
            yield annotation

    def keys(self):
        return set([self.name, self.service.__name__])

    def __repr__(self):
        return "<%s service=%r>" % (self.__class__.__name__, self.keys())

    def fill_connection_pool(self):
        """Fill connections pool"""
        rest_size = self.max_conn - self.pool_size()
        for _ in range(rest_size):
            conn = self.produce_client()
            self.put_back_connection(conn)

    def pool_size(self):
        return len(self.connections)

    def clear(self):
        old_connections = self.connections
        self.connections = self.QueueCls()
        self.generation += 1

        for c in old_connections:
            c.close()

    def get_client_from_pool(self):
        connection = self._get_connection()

        if connection is None:
            return
        if connection.test_connection():  # make sure old connection is usable
            return connection
        else:
            connection.close()

    def _get_connection(self) -> ThriftClient:
        if not self.connections:
            if self.raise_empty:
                raise self.Empty
            return None
        try:
            return self.connections.popleft()
        # When only one connection left, just return None if it
        # has already been popped in another thread.
        except IndexError:
            return None

    def put_back_connection(self, conn):
        assert isinstance(conn, ThriftBaseClient)
        if (
            self.max_conn > 0
            and self.pool_size() < self.max_conn
            and conn.pool_generation == self.generation
        ):
            if self.timeout != conn.get_timeout():
                conn.set_client_timeout(self.timeout * 1000)
            self.connections.append(conn)
            return True
        else:
            conn.close()
            return False

    def produce_client(self, host=None, port=None):
        if host is None and port is None:
            host, port = self.yield_server()
        elif not all((host, port)):
            raise ValueError(
                "host and port should be 'both none' \
                             or 'both provided' "
            )
        return self.connection_class.connect(
            self.service,
            host,
            port,
            self.timeout,
            keepalive=self.keepalive,
            pool_generation=self.generation,
            tracking=self.tracking,
            tracker_factory=self.tracker_factory,
            pool=self,
            use_limit=self.use_limit,
        )

    @client_get_hook
    def get_client(self):
        cli = self.get_client_from_pool()
        
        if cli is not None:
            return cli
        return self.produce_client()

    def __getattr__(self, name):
        method = self.__api_method_cache.get(name)
        if not method:

            def method(*args, **kwds):
                client = self.get_client()
                api = getattr(client, name, None)
                will_put_back = True
                try:
                    if api and callable(api):
                        return api(*args, **kwds)
                    raise AttributeError("%s not found in %s" % (name, client))
                except (client.TTransportException, socket.error):
                    will_put_back = False
                    client.close()
                    raise
                finally:
                    if will_put_back:
                        self.put_back_connection(client)

            self.__api_method_cache[name] = method
        return method

    @contextlib.contextmanager
    def connection_ctx(self, timeout=None):
        client = self.get_client()

        if timeout is not None:
            client.set_client_timeout(timeout * 1000)
        try:
            yield client
            self.put_back_connection(client)
        except (client.TTransportException, socket.error):
            client.close()
            raise
        except Exception:
            self.put_back_connection(client)
            raise

    @contextlib.contextmanager
    def make_temporary_client(self, host, port):
        client = self.produce_client(host, port)
        try:
            yield client
        except Exception:
            raise
        finally:
            client.close()

    def register_after_close_func(self, func):
        self.conn_close_callbacks.append(func)

    def signal_handler(self, signal_name, conn):
        if signal_name == SIGNAL_CLOSE_NAME:
            for cb in self.conn_close_callbacks:
                try:
                    cb(self, conn)
                except:
                    logger.warn("%s Callback failed" % SIGNAL_CLOSE_NAME, exc_info=True)


class ThriftConnnectionPool(BaseThriftConnnection):
    def __init__(
        self,
        service,
        host,
        port,
        timeout=30,
        name=None,
        raise_empty=False,
        max_conn=30,
        connection_class=ThriftClient,
        keepalive=None,
        tracking=False,
        tracker_factory=None,
        use_limit=None,
    ):
        validate_host_port(host, port)
        super(ThriftConnnectionPool, self).__init__(
            service=service,
            timeout=timeout,
            name=name,
            raise_empty=raise_empty,
            max_conn=max_conn,
            connection_class=connection_class,
            keepalive=keepalive,
            tracking=tracking,
            tracker_factory=tracker_factory,
            use_limit=use_limit,
        )
        self.host = host
        self.port = port

    def set_servers(self, server_info):
        host, port = server_info
        validate_host_port(host, port)
        self.host = host
        self.port = port
        self.clear()

    def fill_connection_pool(self):
        raise RuntimeError(
            "{!r} class not support to fill connection pool".format(
                self.__class__.__name__
            )
        )

    def yield_server(self):
        return self.host, self.port
