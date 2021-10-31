import logging
import sys

logger = logging.getLogger("mediapy")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
good_format = logging.Formatter('%(asctime)s pid=%(process)d %(filename)s:%(lineno)s %(funcName)s [%(name)s]-%(levelname)s: %(message)s')
handler.setFormatter(good_format)
logger.addHandler(handler)
