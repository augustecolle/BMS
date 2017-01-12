import logging
import logconf
import logging.config
import imp
import signal
import time
import sys
imp.reload(logconf)

logging.config.dictConfig(logconf.LOGGING)
logger = logging.getLogger('BMS')
   
def signal_handler(signal_s, frame):
    logger.critical('EXITING SYSTEM')
    sys.exit(1)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

i = 0
while True:
    time.sleep(10)
    logger.debug('Sitting in loop %d', i)
    i = i + 1


