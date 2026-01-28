import time
import logging
from collections import deque
from datetime import datetime, timezone

from config import *


MAX_LOG_SECONDS = 86400  # 24 hours in seconds
class MemoryHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.buffer = deque()

    def emit(self, record):
        log_entry = self.format(record)
        self.buffer.append((time.time(), log_entry))
        self.cleanup()

    def cleanup(self):
        cutoff = time.time() - MAX_LOG_SECONDS
        while self.buffer and self.buffer[0][0] < cutoff:
            self.buffer.popleft()

    def get_logs(self):
        self.cleanup()
        return [log for _, log in self.buffer]


def init_logger():
    _logger = logging.getLogger("server")
    _logger.setLevel(logging.INFO)

    curr_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")
    file_handler = logging.FileHandler(f"./logs/{curr_time}.log", encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    memory_handler = MemoryHandler()
    memory_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    _logger.addHandler(file_handler)
    _logger.addHandler(memory_handler)
    return _logger

logger = init_logger()


def update_log_file():
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.flush()
            logger.removeHandler(handler)
            handler.close()

    curr_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")
    file_handler = logging.FileHandler(f"{LOG_DIR}/{curr_time}.log", encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger.addHandler(file_handler)
