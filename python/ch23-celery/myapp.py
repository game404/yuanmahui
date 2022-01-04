import time

from celery import Celery

app = Celery(
    'myapp',
    broker='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    # ## add result backend here if needed.
    backend='rpc'
)


@app.task
def add(x, y):
    time.sleep(1)
    return x + y


if __name__ == '__main__':
    app.start()
