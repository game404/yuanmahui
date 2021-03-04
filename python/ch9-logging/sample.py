import logging
import sys

print("haha")
print("fatal error", file=sys.stderr)
sys.stderr.write("fatal error\n")

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(name)-10s %(asctime)s %(message)s')
lang = {"name": "python", "age":20}
logging.info('This is a info message %s', lang)
logging.debug('This is a debug message')
logging.warning('This is a warning message')


logger = logging.getLogger(__name__)
logger.warning('This is a warning')
