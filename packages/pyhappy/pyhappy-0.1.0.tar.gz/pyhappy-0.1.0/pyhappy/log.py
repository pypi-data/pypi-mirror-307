"""
This module provides an extensible logging framework that supports multiple logging mechanisms, including file-based, console-based,
and event-driven logging. The framework leverages customizable configurations and employs log levels, batching, and rotation features
to efficiently manage and retain logs. Additionally, it supports context-based and function-level logging for detailed traceability.

Classes:
    - `BufferProtocol`: Abstract base class for buffer implementations, defining buffer operations.
    - `LogLevel`: Enum representing different logging levels (TRACE, DEBUG, INFO, etc.).
    - `LogFormat`: Defines common logging format templates.
    - `BaseLoggingConfig`: Base configuration for any logger, with options for format, retention, and worker settings.
    - `FileLoggingConfig`: Extends `BaseLoggingConfig` for file logging configurations (directory, size, rotation).
    - `ConsoleLoggingConfig`: Extends `BaseLoggingConfig` for console logging, with color and time display options.
    - `EventLoggingConfig`, `QueueLoggingConfig`, `BatchLoggingConfig`, `BufferLoggingConfig`: Configurations for advanced logging strategies.
    - `BaseLogger`: Abstract base logger class implementing common functionality for various loggers.
    - `FileLogger`: A logger for managing log files, supporting rotation and backup.
    - `ConsoleLogger`: A logger for console output with customizable format and color.

Functions:
    - `log_function`: Decorator to log entry and exit of a function, capturing errors as well.
    - `log_context`: Context manager for logging at the beginning and end of a code block, capturing exceptions if they occur.

Usage Examples:
    - Configure a `FileLogger` with file rotation and retention.
    - Configure a `ConsoleLogger` with colored output and use `log_function` decorator for function logging.
    - Use `log_context` to manage and trace log entries within specific code blocks.

This module is designed for applications requiring structured, high-performance logging capabilities, including projects with
multi-threaded or multi-process requirements.
"""

import inspect
import multiprocessing as mp
import shutil
import sys
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
# Enums for log configuration
from enum import Enum
from pathlib import Path
from queue import Queue
from types import TracebackType
from typing import Callable, List, Union, Optional, Type, Dict, Generic, TypeVar, Any

from loguru import logger as loguru_logger

T = TypeVar('T')


class BufferProtocol(ABC, Generic[T]):
    @property
    @abstractmethod
    def id(self) -> Any:
        """Get buffer unique identifier."""

    @property
    @abstractmethod
    def size(self) -> int:
        """Get current buffer size."""

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """Check if buffer is empty."""

    @property
    @abstractmethod
    def is_full(self) -> bool:
        """Check if buffer is at capacity."""

    @abstractmethod
    def transaction(self):
        """Context manager for atomic operations."""

    @abstractmethod
    def push(self, item: T) -> None:
        """Push item to buffer."""

    @abstractmethod
    def pop(self) -> T:
        """Pop item from buffer."""

    @abstractmethod
    def clear(self) -> None:
        """Clear all items from buffer."""

    @abstractmethod
    def flush(self) -> None:
        """Flush buffer contents based on configuration."""


class LogLevel(Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogFormat:
    """Contains predefined logging formats."""
    UNIX = "[{level}]  [{time.iso}]: {extra[func_name]} {message} {time.iso}"
    HAPPY = "{time:YYYY-MM-DD at HH:mm:ss} | module {extra[module_name]} | line {extra[lineno]} | function {extra[func_name]} | <bold>{level}</bold> | {message}"
    MINIMAL = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"


@dataclass
class BaseLoggingConfig:
    """Base configuration for all logging types."""
    format_style: Optional[str] = None
    retention_days: int = 14
    max_workers: Optional[int] = None
    correlation_id: Optional[str] = None


@dataclass
class FileLoggingConfig(BaseLoggingConfig):
    """Configuration for file-based logging."""
    log_dir: Path = Path("logs")
    suffix: str = ".log"
    prefix: str = ""
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    rotate_on_size: bool = True


@dataclass
class ConsoleLoggingConfig(BaseLoggingConfig):
    """Configuration for console-based logging."""
    colored: bool = True
    show_time: bool = True


@dataclass
class EventLoggingConfig(BaseLoggingConfig):
    """Configuration for event-based logging."""
    event_types: List[str] = None  # List of event types to monitor
    async_dispatch: bool = False
    batch_size: int = 100
    flush_interval: float = 1.0  # seconds


@dataclass
class QueueLoggingConfig(BaseLoggingConfig):
    """Configuration for queue-based logging."""
    queue_size: int = 1000
    workers: int = 4
    batch_size: int = 50
    flush_interval: float = 0.5  # seconds


@dataclass
class BatchLoggingConfig(BaseLoggingConfig):
    """Configuration for batch logging."""
    batch_size: int = 100
    flush_interval: float = 1.0  # seconds
    max_batch_age: float = 5.0  # seconds


class BufferConfig:
    pass


@dataclass
class BufferLoggingConfig(BaseLoggingConfig):
    """Configuration for buffer-based logging."""
    buffer_config: BufferConfig = field(default_factory=BufferConfig)
    flush_interval: float = 1.0  # seconds
    max_retries: int = 3


class BaseLogger(ABC):
    """Base logger class implementing common functionality."""

    def __init__(self, config: BaseLoggingConfig):
        self.config = config
        self.max_workers = config.max_workers or mp.cpu_count()
        self._format = config.format_style or LogFormat.MINIMAL
        self._init_workers()
        self._configure_log_levels()
        self._message_queue = Queue()

    def _init_workers(self) -> None:
        """Initialize thread and process pools."""
        self._thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self._process_pool = ProcessPoolExecutor(max_workers=self.max_workers)

    @staticmethod
    def _configure_log_levels() -> None:
        """Configure custom log levels with icons and colors."""
        level_styles = {
            LogLevel.TRACE: ("🔮", "<cyan>"),
            LogLevel.DEBUG: ("🐞", "<green><bold>"),
            LogLevel.INFO: ("ℹ️", "<blue><bold>"),
            LogLevel.WARNING: ("⚠️", "<yellow><bold>"),
            LogLevel.ERROR: ("❌", "<red>"),
            LogLevel.CRITICAL: ("☠️", "<red><bold>"),
        }

        for level, (icon, color) in level_styles.items():
            loguru_logger.level(name=level.value, icon=icon, color=color)

    @abstractmethod
    def log(self, message: str, level: Union[str, LogLevel] = LogLevel.INFO, **kwargs) -> None:
        """Log a message with the specified level."""
        pass

    @staticmethod
    def _get_caller_info() -> Dict[str, str]:
        """Get information about the calling function."""
        frame = inspect.currentframe()
        caller = frame.f_back.f_back if frame and frame.f_back else None

        if caller:
            return {
                'function': caller.f_code.co_name,
                'filename': caller.f_code.co_filename,
                'lineno': caller.f_lineno
            }
        return {}

    def __enter__(self) -> 'BaseLogger':
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        self.cleanup()

    async def __aenter__(self) -> 'BaseLogger':
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_val: Optional[BaseException],
                        exc_tb: Optional[TracebackType]) -> None:
        self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources."""
        self._thread_pool.shutdown(wait=True)
        self._process_pool.shutdown(wait=True)


class FileLogger(BaseLogger):
    """File-based logger implementation."""

    def __init__(self, config: FileLoggingConfig):
        super().__init__(config)
        self.config: FileLoggingConfig = config
        self._setup_log_directory()
        self._setup_logging()

    def _setup_log_directory(self) -> None:
        """Create log directory if it doesn't exist."""
        self.config.log_dir.mkdir(parents=True, exist_ok=True)

    def _setup_logging(self) -> None:
        """Configure file logging."""
        log_file = self.config.log_dir / f"{self.config.prefix}{datetime.now():%Y%m%d}{self.config.suffix}"

        loguru_logger.add(
            sink=str(log_file),
            rotation=self.config.max_bytes if self.config.rotate_on_size else "1 day",
            retention=f"{self.config.retention_days} days",
            format=self._format,
            enqueue=True,
            backtrace=True,
            diagnose=True
        )

    # noinspection DuplicatedCode
    def log(self, message: str, level: Union[str, LogLevel] = LogLevel.INFO, **kwargs) -> None:
        """Log a message to file with the specified level."""
        caller_info = self._get_caller_info()

        if isinstance(level, LogLevel):
            level = level.value

        extra = {
            **caller_info,
            **kwargs,
            'correlation_id': self.config.correlation_id
        }

        loguru_logger.bind(**extra).opt(depth=1).log(level, message)

    def backup(self, backup_dir: Optional[Path] = None) -> None:
        """Create a backup of log files."""
        backup_path = backup_dir or self.config.log_dir / "backups"
        backup_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for log_file in self.config.log_dir.glob(f"{self.config.prefix}*{self.config.suffix}"):
            if log_file.is_file():
                backup_file = backup_path / f"{log_file.stem}_{timestamp}{log_file.suffix}"
                shutil.copy2(log_file, backup_file)

    def clear(self, days: Optional[int] = None) -> None:
        """Clear log files older than specified days."""
        retention_days = days or self.config.retention_days
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        for log_file in self.config.log_dir.glob(f"{self.config.prefix}*{self.config.suffix}"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink()


class ConsoleLogger(BaseLogger):
    """Console-based logger implementation."""

    def __init__(self, config: ConsoleLoggingConfig):
        super().__init__(config)
        self.config: ConsoleLoggingConfig = config
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure console logging."""
        loguru_logger.add(
            sink=sys.stderr,
            format=self._format,
            colorize=self.config.colored,
            enqueue=True
        )

    # noinspection DuplicatedCode
    def log(self, message: str, level: Union[str, LogLevel] = LogLevel.INFO, **kwargs) -> None:
        """Log a message to console with the specified level."""
        caller_info = self._get_caller_info()

        if isinstance(level, LogLevel):
            level = level.value

        extra = {
            **caller_info,
            **kwargs,
            'correlation_id': self.config.correlation_id
        }

        loguru_logger.bind(**extra).opt(depth=1).log(level, message)


def log_function(logger: BaseLogger, level: Union[str, LogLevel] = LogLevel.INFO):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            logger.log(f"Entering function: {func_name}", level)
            try:
                result = func(*args, **kwargs)
                logger.log(f"Exiting function: {func_name}", level)
                return result
            except Exception as e:
                logger.log(f"Error in function {func_name}: {str(e)}", LogLevel.ERROR)
                raise

        return wrapper

    return decorator


@contextmanager
def log_context(logger: BaseLogger, context_name: str, level: Union[str, LogLevel] = LogLevel.INFO):
    logger.log(f"Entering context: {context_name}", level)
    try:
        yield
    except Exception as e:
        logger.log(f"Error in context {context_name}: {str(e)}", LogLevel.ERROR)
        raise
    finally:
        logger.log(f"Exiting context: {context_name}", level)


if __name__ == '__main__':
    # # File logging example
    # file_config = FileLoggingConfig(
    #     log_dir=Path("logs"),
    #     format_style=LogFormat.MINIMAL,
    #     retention_days=30,
    #     correlation_id="session-123"
    # )
    # file_logger = FileLogger(file_config)

    # Console logging example
    console_config = ConsoleLoggingConfig(
        colored=False,
        format_style=LogFormat.MINIMAL
    )
    console_logger = ConsoleLogger(console_config)
    console_logger.log("Test console log message", LogLevel.INFO)


    # Using the decorator
    @log_function(console_logger)
    def some_function():
        # Function code here
        pass

    # Using the context manager
    # with log_context(file_logger, "data_processing", LogLevel.INFO):
    #     # Processing code here
    #     print("Processing data...")
    #     pass
    #
    # # Direct logging
    # file_logger.log("Processing started", LogLevel.INFO)
