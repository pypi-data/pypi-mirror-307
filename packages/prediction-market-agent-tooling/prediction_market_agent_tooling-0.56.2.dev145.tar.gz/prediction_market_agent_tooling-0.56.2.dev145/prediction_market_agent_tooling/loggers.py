import builtins
import logging
import typing as t
import warnings
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class LogFormat(str, Enum):
    GCP = "gcp"


class LogLevel(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class LogConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    LOG_FORMAT: LogFormat = LogFormat.GCP
    LOG_LEVEL: LogLevel = LogLevel.INFO


class NoNewLineStreamHandler(logging.StreamHandler):  # type: ignore # StreamHandler is not typed in the standard library.
    def format(self, record: logging.LogRecord) -> str:
        return super().format(record).replace("\n", " ")


GCP_LOG_LOGGING_FORMAT, GCP_LOG_FORMAT_LOGGING_DATEFMT = (
    "%(levelname).1s%(asctime)s %(process)d %(name)s:%(pathname)s:%(funcName)s:%(lineno)d] %(message)s"
), "%m%d %H:%M:%S"


def patch_logger() -> None:
    """
    Function to patch loggers according to the deployed environment.
    Patches Python's default logger, warnings library and also monkey-patch print function as many libraries just use it.
    """
    if not getattr(logger, "_patched", False):
        logger._patched = True  # type: ignore[attr-defined] # Hacky way to store a flag on the logger object, to not patch it multiple times.
    else:
        return

    config = LogConfig()

    if config.LOG_FORMAT == LogFormat.GCP:
        format_logging = GCP_LOG_LOGGING_FORMAT
        datefmt_logging = GCP_LOG_FORMAT_LOGGING_DATEFMT
        print_logging = print_using_logger
        handlers = [NoNewLineStreamHandler()]

    else:
        raise ValueError(f"Unknown log format: {config.LOG_FORMAT}")

    # Change built-in logging.
    logging.basicConfig(
        level=config.LOG_LEVEL.value,
        format=format_logging,
        datefmt=datefmt_logging,
        handlers=handlers,
    )

    # Change warning formatting to a simpler one (no source code in a new line).
    warnings.formatwarning = simple_warning_format
    # Use logging module for warnings.
    logging.captureWarnings(True)

    # Use logger for prints.
    builtins.print = print_logging  # type: ignore[assignment] # Monkey patching, it's messy but it works.

    logger.info(f"Patched logger for {config.LOG_FORMAT.value} format.")


def print_using_logger(
    *values: object,
    sep: str = " ",
    end: str = "\n",
    **kwargs: t.Any,
) -> None:
    message = sep.join(map(str, values)) + end
    message = message.strip().replace(
        "\n", "\\n"
    )  # Escape new lines, because otherwise logs will be broken.
    logger.info(message)


def simple_warning_format(message, category, filename, lineno, line=None):  # type: ignore[no-untyped-def] # Not typed in the standard library neither.
    return f"{category.__name__}: {message}".strip().replace(
        "\n", "\\n"
    )  # Escape new lines, because otherwise logs will be broken.


logger = logging.getLogger("prediction-market-agent-tooling")

patch_logger()
