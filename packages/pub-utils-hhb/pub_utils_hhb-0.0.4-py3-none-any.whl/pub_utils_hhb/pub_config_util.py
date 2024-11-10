import os
import json

from typing import Any
from logging import Logger

from pub_utils_hhb.pub_args_util import Arg, validate_kwargs
from pub_utils_hhb.pub_common_util import singleton

__all__ = [
    'JsonFile',
    'ReadOnlyJsonFile',
    'ConfigFile',
    'ConfigFileManager',
]


class JsonFile:
    def __init__(self, **kwargs):
        # params
        path = kwargs['path']
        logger = kwargs['logger']
        ignore_file_not_found = kwargs['ignore_file_not_found']

        self._content = {}
        self._path = path
        self._file = os.path.split(path)[1]
        self._file_exist = os.path.exists(self._path)
        self._ignore_file_not_found = ignore_file_not_found
        self._logger = logger if logger else self._init_default_logger()

    def get_path(self) -> str:
        return self._path

    def is_file_exists(self) -> bool:
        return self._file_exist

    def get(self, *keys, default_value=None) -> Any:
        val = self._content
        try:
            for key in keys:
                val = val[key]
        except KeyError as e:
            self._logger.warning('get value occurs KeyError, keys: %s, return default value: %s', keys, default_value)
            return default_value

        return val

    def set(self, key, val) -> None:
        self._content[key] = val

    def set_and_dump(self, key, val) -> None:
        self.set(key, val)
        self.dump()

    def load(self) -> None:
        try:
            with open(self._path, mode='r', encoding='utf-8') as f:
                self._content = json.loads(f.read())
            self._logger.debug('load json file ok: %s', self._path)
        except FileNotFoundError as e:
            if self._ignore_file_not_found:
                self._content = {}
                self._logger.warning('load json file failed: %s, file not found, ignore', self._path)
                return
            raise FileNotFoundError(f'load json file failed: {self._path}, file not found') from e

    def dump(self) -> None:
        try:
            with open(self._path, mode='w', encoding='utf-8') as f:
                f.write(json.dumps(self._content, ensure_ascii=False, indent=4))
            self._logger.debug('dump json file ok: %s', self._path)
        except Exception as e:
            raise Exception(f'dump json file failed: {self._path}') from e

    def reload(self) -> None:
        self.load()

    @staticmethod
    def _init_default_logger() -> Logger:
        from pub_utils_hhb.pub_logger_util import LOGGER_FORMAT_1, LoggerManager

        logger_manager = LoggerManager()
        logger = logger_manager.get_logger(logger_name=f'{__class__.__name__}_logger')

        logger.set_logger_format(LOGGER_FORMAT_1)
        logger.build_file_handler()
        logger.build_stream_handler()
        return logger


class ReadOnlyJsonFile(JsonFile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set(self, key, val):
        raise NotImplementedError('function is unsupported in ReadOnlyJsonFile')

    def set_and_dump(self, key, val):
        raise NotImplementedError('function is unsupported in ReadOnlyJsonFile')

    def dump(self):
        raise NotImplementedError('function is unsupported in ReadOnlyJsonFile')


class ConfigFile(JsonFile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@singleton
class ConfigFileManager:
    cfg_file_instances = {}  # path -> ConfigFile object

    expected_kwargs = [
        Arg('path').set_arg_type(str).set_required(True),
        Arg('read_only').set_arg_type(bool).set_default_value(False),
        Arg('ignore_file_not_found').set_arg_type(bool).set_default_value(False),
        Arg('logger').set_arg_type(Logger).set_default_value(None),
    ]

    @classmethod
    def get_config_file(cls, **kwargs) -> ConfigFile:
        """
        Get or create a ConfigFile object.

        :param kwargs: ConfigFileManager.expected_args
        :return: ConfigFile object
        """
        validate_kwargs(expected=cls.expected_kwargs, actual=kwargs)

        path = kwargs['path']
        if path not in cls.cfg_file_instances:
            read_only = kwargs['read_only']
            if read_only:
                cls.cfg_file_instances[path] = ReadOnlyJsonFile(**kwargs)
            else:
                cls.cfg_file_instances[path] = ConfigFile(**kwargs)

        return cls.cfg_file_instances[path]

# --------------------------------------------------
#                   Usage Example
# --------------------------------------------------
# config_file_manager = ConfigFileManager()
# config = config_file_manager.get_config_file(path)
# config.load()
# --------------------------------------------------
