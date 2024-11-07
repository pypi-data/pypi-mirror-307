from typing import TypeVar, Generic
from py_service_client.common.thrift_connection_pool import ThriftConnnectionPool

T = TypeVar("T")

class BaseClient(Generic[T]): 
    def __init__(self, service, host, port, timeout = 5):
        self.pool = ThriftConnnectionPool(
            service,
            host,
            port,
           int(timeout)
        )

        # with ThriftConnectionPool(create_client, pool_size=10, timeout=5) as pool:
        #     with pool.get_connection() as client:
        #     # Use client
        # pass

        self.client:T = self.pool

    def get_client(self) -> T:
        return self.pool.get_client()
