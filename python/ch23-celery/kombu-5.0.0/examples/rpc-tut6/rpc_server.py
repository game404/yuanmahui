#!/usr/bin/env python

from kombu import Connection, Queue
from kombu.mixins import ConsumerProducerMixin

rpc_queue = Queue('rpc_queue')


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


class Worker(ConsumerProducerMixin):

    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        # 创建consumer接收请求
        return [Consumer(
            queues=[rpc_queue],
            on_message=self.on_request,
            accept={'application/json'},
            prefetch_count=1,
        )]

    def on_request(self, message):
        # 处理远程调用请求
        n = message.payload['n']
        print(f' [.] fib({n})')
        # 业务计算
        result = fib(n)
        # 响应请求(使用新的producer回应)
        self.producer.publish(
            {'result': result},
            # 读取来源地址，进行回应
            exchange='', routing_key=message.properties['reply_to'],
            # 请求和响应关联
            correlation_id=message.properties['correlation_id'],
            serializer='json',
            retry=True,
        )
        # 注意别忘记ack
        message.ack()


def start_worker(broker_url):
    connection = Connection(broker_url)
    print(' [x] Awaiting RPC requests')
    worker = Worker(connection)
    worker.run()


if __name__ == '__main__':
    try:
        start_worker('pyamqp://')
    except KeyboardInterrupt:
        pass
