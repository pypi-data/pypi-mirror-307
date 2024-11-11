import logging
import logging.config

import pkg_resources
from computenestcli.common.logging_type import LoggingType

logging_initialized = False


def setup_logging(config_file='log.conf'):
    """Set up logging configuration from a configuration file."""
    global logging_initialized
    if not logging_initialized:
        # 获取配置文件的路径
        config_path = pkg_resources.resource_filename(__name__, config_file)
        logging.config.fileConfig(config_path)


def get_logger(name):
    """Get a logger with the specified name."""
    return logging.getLogger(name)


def get_developer_logger():
    setup_logging()
    return get_logger(LoggingType.DEVELOPER.value)


def get_user_logger():
    setup_logging()
    return get_logger(LoggingType.USER.value)
