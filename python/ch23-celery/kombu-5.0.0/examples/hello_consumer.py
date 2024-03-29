from kombu import Connection  # noqa


with Connection('amqp://guest:guest@localhost:5672//') as conn:
    # 简单易用(注意名称和producer一致)
    simple_queue = conn.SimpleQueue('simple_queue')
    message = simple_queue.get(block=True, timeout=1)
    print(f'Received: {message.payload}')
    message.ack()
    simple_queue.close()
