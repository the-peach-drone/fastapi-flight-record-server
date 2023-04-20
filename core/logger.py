from pathlib     import Path
from loguru      import logger
from core.config import Settings

import logging, sys, json

# Server Setting
settings = Settings()

class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id = 'app')
        log.opt(depth = depth, exception = record.exc_info).log(level, record.getMessage())

class CustomizeLogger:
    @classmethod
    def make_logger(cls, config_path: Path):

        # Disable uvicorn logger
        uvicorn_error = logging.getLogger("uvicorn.error")
        uvicorn_error.propagate = False

        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')

        logger = cls.customize_logging(
            level    = logging_config.get('level'),
            rotation = logging_config.get('rotation'),
            format   = logging_config.get('format')
        )
        return logger

    @classmethod
    def customize_logging(cls, level: str, rotation: str, format: str):
        logger.remove() # Remove default logger
        
        logger.add(sys.stdout, enqueue = True, backtrace = True, level = level.upper(), format = format)                                  # Add stdout logger
        logger.add(settings.LOG_FILENAME, rotation = rotation, enqueue = True, backtrace = True, level = level.upper(), format = format)  # Add file logger
        logging.basicConfig( handlers = [ InterceptHandler() ], level = 0 )

        return logger.bind(request_id = 'app', method = None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
