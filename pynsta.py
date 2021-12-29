import time
import random
import os

from logger import log
from bot import Bot


if __name__ == '__main__':
    try:
        bot = Bot()
        bot()
    except Exception as e:
        log.error("exception caught", extra={"error": e})
        log.debug("", extra={"trace": e.__traceback__})
        exit(1)
    except KeyboardInterrupt:
        pass
