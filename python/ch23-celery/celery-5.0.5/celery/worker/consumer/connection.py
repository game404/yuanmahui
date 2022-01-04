"""Consumer Broker Connection Bootstep."""
from kombu.common import ignore_errors

from celery import bootsteps
from celery.utils.log import get_logger

__all__ = ('Connection',)

logger = get_logger(__name__)
info = logger.info


class Connection(bootsteps.StartStopStep):
    """Service managing the consumer broker connection."""

    def __init__(self, c, **kwargs):
        c.connection = None
        super().__init__(c, **kwargs)

    def start(self, c):
        # 创建连接
        c.connection = c.connect()
        info('Connected to %s', c.connection.as_uri())

    def shutdown(self, c):
        # We must set self.connection to None here, so
        # that the green pidbox thread exits.
        connection, c.connection = c.connection, None
        if connection:
            # 关闭连接
            ignore_errors(connection, connection.close)

    def info(self, c):
        params = 'N/A'
        if c.connection:
            # 打印连接信息
            params = c.connection.info()
            # 脱敏
            params.pop('password', None)  # don't send password.
        return {'broker': params}
