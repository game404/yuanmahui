"""
Example that use memory transport for message produce.
"""
import time

from kombu import Connection, Exchange, Queue, Consumer

media_exchange = Exchange('media', 'direct')
video_queue = Queue('video', exchange=media_exchange, routing_key='video')
task_queues = [video_queue]


def handle_message(body, message):
    print(f"{time.time()} RECEIVED MESSAGE: {body!r}")
    message.ack()


# 基于内存的传输连接，可以用于单元测试等
# producer和consumer需要在同一个进程
connection = Connection("memory:///")
consumer = Consumer(connection, task_queues, callbacks=[handle_message])

producer = connection.Producer(serializer='json')
producer.publish({"foo": "bar"}, exchange=media_exchange, routing_key='video', declare=task_queues)
consumer.consume()
connection.drain_events()
