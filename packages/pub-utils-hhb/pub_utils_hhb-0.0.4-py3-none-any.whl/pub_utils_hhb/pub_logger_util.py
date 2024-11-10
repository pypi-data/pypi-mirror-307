import os
import logging

from pub_utils_hhb.pub_common_util import get_sub_dir, singleton
from pub_utils_hhb.pub_time_util import now_str

__all__ = [
    'LOGGER_FORMAT_1',
    'LOGGER_FORMAT_2',
    'LOGGER_FORMAT_3',
    'LoggerManager'
]

LOGGER_FORMAT_1 = ('[%(asctime)s.%(msecs)03d] [%(filename)s:%(lineno)d] [%(levelname)s] [%(threadName)s] %(message)s',
                   '%Y/%m/%d %H:%M:%S')
LOGGER_FORMAT_2 = ('[%(asctime)s.%(msecs)03d][%(levelname)s] %(message)s', '%Y/%m/%d %H:%M:%S')
LOGGER_FORMAT_3 = ('%(asctime)s %(levelname)s %(message)s', '%H:%M:%S')


class Logger(logging.Logger):
    DEFAULT_FORMAT = LOGGER_FORMAT_1

    def __init__(self, name: str):
        super().__init__(name)

        self._log_dir_path = get_sub_dir('log')
        self._log_file_path = os.path.join(self._log_dir_path, now_str(fmt='%Y-%m-%d %H-%M-%S') + f' ({name}).log')
        self._fmt = logging.Formatter(*Logger.DEFAULT_FORMAT)

        if not os.path.exists(self._log_dir_path):
            os.mkdir(self._log_dir_path)

    def set_logger_format(self, fmt: tuple):
        self._fmt = logging.Formatter(*fmt)

    def build_stream_handler(self, log_level=logging.INFO):
        """
        Build logger handler for console.
        If logs are expected to print on QTextBrowser,
        this function must be called after sys.stderr = EmittingStr()
        """
        sh = logging.StreamHandler()
        sh.setFormatter(self._fmt)
        sh.setLevel(log_level)
        self.addHandler(sh)

    def build_file_handler(self, log_level=logging.DEBUG):
        """
        Build logger handler for file.
        """
        fh = logging.FileHandler(self._log_file_path, encoding='utf-8')
        fh.setFormatter(self._fmt)
        fh.setLevel(log_level)
        self.addHandler(fh)


@singleton
class LoggerManager:
    logger_instances = {}  # logger_name -> Logger object

    @classmethod
    def get_logger(cls, logger_name: str = 'main_logger') -> Logger:
        if logger_name not in cls.logger_instances:
            cls.logger_instances[logger_name] = Logger(logger_name)

        return cls.logger_instances.get(logger_name)

# --------------------------------------------------
#                   Usage Example
# --------------------------------------------------
# logger_manager = LoggerManager()
# logger = logger_manager.get_logger()
# logger.set_logger_format(Logger.FORMAT_1)
# logger.build_file_handler()
# logger.build_stream_handler()
# --------------------------------------------------
