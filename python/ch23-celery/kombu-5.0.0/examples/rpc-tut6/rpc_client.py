#!/usr/bin/env python

from kombu import Connection, Producer, Consumer, Queue, uuid


class FibonacciRpcClient:

    def __init__(self, connection):
        self.connection = connection
        # 响应队列
        self.callback_queue = Queue(uuid(), exclusive=True, auto_delete=True)

    def on_response(self, message):
        if message.properties['correlation_id'] == self.correlation_id:
            self.response = message.payload['result']

    def call(self, n):
        self.response = None
        # 唯一标识匹配请求和响应，每次请求都生成
        self.correlation_id = uuid()
        # 作为生产者发送请求
        with Producer(self.connection) as producer:
            producer.publish(
                {'n': n},
                # 使用默认exchange
                exchange='',
                # routing_key和Queue一致
                routing_key='rpc_queue',
                declare=[self.callback_queue],
                # 回应的queue
                reply_to=self.callback_queue.name,
                # 业务ID
                correlation_id=self.correlation_id,
            )
        # 作为消费者接收响应
        with Consumer(self.connection,
                      on_message=self.on_response,
                      queues=[self.callback_queue], no_ack=True):
            while self.response is None:
                # 持续监听，直到回应（阻塞）
                # TODO 非阻塞实现
                self.connection.drain_events()
        return self.response


def main(broker_url):
    connection = Connection(broker_url)
    fibonacci_rpc = FibonacciRpcClient(connection)
    print(' [x] Requesting fib(30)')
    # 使用消息队列实现RPC
    response = fibonacci_rpc.call(30)
    print(f' [.] Got {response!r}')


if __name__ == '__main__':
    main('pyamqp://')
