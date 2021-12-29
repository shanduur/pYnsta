import logging
import os
from pythonjsonlogger import jsonlogger


log = logging.getLogger('pynsta')
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(levelname)s %(message)s')
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

lvl = os.getenv('DEBUG')
if lvl:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)
