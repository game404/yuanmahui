import logging
import threading
import time


def thread_function(name):
    tid = threading.get_ident()
    # tid = threading.get_native_id()
    logging.info("Thread %s: starting %d", name, tid)
    time.sleep(2)
    logging.info("Thread %s: finishing %d", name, tid)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main %d   : before creating thread", threading.get_ident())
    for i in range(3):
        x = threading.Thread(target=thread_function, args=(i,))
        logging.info("Main    : before running thread")
        x.start()
        logging.info("Main    : wait for the thread to finish")
        # x.join()
    logging.info("Main    : all done")
