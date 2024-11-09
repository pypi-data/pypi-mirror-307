"""
Utility module providing collection-related functionality including file creation, recycling bin management,
and enhanced data structures with operator support.
"""

from __future__ import annotations

import asyncio
# noinspection PyCompatibility
# noinspection PyCompatibility
import imghdr
import inspect
import json
import logging
import os
import queue
import shutil
import threading
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from contextlib import contextmanager, asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import List, Dict, Any, Generator
from typing import ParamSpec
from typing import TypeVar, Callable, Union

import pydub.generators
from PIL import Image
from moviepy.editor import ImageSequenceClip, ImageClip

from pyhappy.exceptions import (StorageFullError, RecycleBinError, ItemNotFoundError, RestoreError)

R = TypeVar('R')
P = ParamSpec('P')
T = TypeVar('T')


def _to_numeric(value: Any) -> Union[int, float]:
    """Convert value to a numeric type suitable for bitwise operations"""
    if isinstance(value, bool):
        return int(value)
    elif isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"Cannot convert string '{value}' to numeric type")
    raise ValueError(f"Cannot convert type {type(value)} to numeric type")


def is_image(path):
    return imghdr.what(path)


def copy_dir(src, dst, **kwargs):
    shutil.copytree(src, dst, symlinks=True, copy_function=shutil.copy2, **kwargs)


def copy_file(src, dst):
    shutil.copy(src, dst)


def copy_dir_to_same_depth(src: os.PathLike, dst: os.PathLike, **kwargs):
    _dst = os.path.join(dst, os.path.basename(src))
    os.makedirs(os.path.dirname(_dst), exist_ok=True)
    shutil.copytree(src, _dst, **kwargs)


def _random_color() -> tuple[int, int, int]:
    import random
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def _create_file(filename, header, size, content):
    """
    Internal method to create a dummy file with specified header and size.

    :param filename: Name of the file to create.
    :param header: Header bytes of the file.
    :param size: Total size of the file in bytes.
    :param content: Content to fill the file.
    """
    try:
        with open(filename, 'wb') as f:
            f.write(header)
            remaining_size = size - len(header)
            if remaining_size > 0:
                f.write(content * (remaining_size // len(content)) +
                        content[:remaining_size % len(content)])
    except Exception as e:
        print(f"Failed to create file {filename}: {e}")


class FileCreator(ABC):
    """
    Abstract base class that defines the template for creating a dummy file.
    """

    FILE_HEADERS = {
        '.pdf': b'%PDF-1.4\n%',
        '.epub': b'PK\x03\x04',
        '.docx': b'PK\x03\x04',
        '.xlsx': b'PK\x03\x04',
        '.txt': b'',
        '.jpg': b'\xFF\xD8\xFF',
        '.png': b'\x89PNG\r\n\x1a\n',
        '.gif': b'GIF89a',
        '.zip': b'PK\x03\x04',
        '.mp3': b'ID3',  # MP3 audio file
        '.wav': b'RIFF',  # WAV audio file
        '.mp4': b'ftyp',  # MP4 video file
        '.avi': b'RIFF',  # AVI video file
        '.mkv': b'\x1A\x45\xDF\xA3',  # MKV video file
        '.svg': b'<?xml version="1.0"?>',  # SVG file
        '.bmp': b'BM',  # BMP image file
        '.tiff': b'II*\x00',  # TIFF image file
        '.tar': b'ustar',  # TAR file
        '.rar': b'Rar!',  # RAR file
        '.7z': b'7z\xBC\xAF\x27\x1C',  # 7z file
    }

    def __init__(self, extension, default_size=1024, default_content=None):
        """
        Initialize the FileCreator instance.

        :param extension: File extension including dot (e.g., '.pdf')
        :param default_size: Default size of the dummy file in bytes.
        :param default_content: Default content to fill the dummy file.
        """
        self.extension = extension
        self.default_size = default_size
        self.default_content = default_content or b'0'
        self.created_files = []

    def create_file(self, filename=None, size=None, content=None):
        """
        Template method to create a dummy file.

        :param filename: Name of the file to create.
        :param size: Size of the file in bytes.
        :param content: Content to fill the file.
        """
        filename = filename or self.default_filename
        size = size or self.default_size

        header = self.header
        if callable(header):  # A bug where sometimes returns callable for custom files
            header = header()

        content = content.encode() if isinstance(content, str) else content or self.default_content
        _create_file(filename, header, size, content)
        self.created_files.append(filename)
        print(f"Created dummy file: {filename} ({size} bytes)")

    @property
    def header(self):
        """Get the header bytes for the file type."""
        return self.FILE_HEADERS[self.extension]

    @property
    def default_filename(self):
        """Get the default filename for the file type."""
        return f'dummy{self.extension}'

    def list_created_files(self):
        """
        List all created dummy files.

        :return: List of filenames.
        """
        return self.created_files.copy()

    def reset(self):
        """Reset the list of created files."""
        self.created_files = []

    def __repr__(self):
        return f"<{self.__class__.__name__} created: {len(self.created_files)} files>"

    def __str__(self):
        return f"{self.__class__.__name__} Utility - {len(self.created_files)} files created."


# Concrete File Creators - simplified!
class PDFFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.pdf', default_size, default_content)


class EPUBFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.epub', default_size, default_content)


class DOCXFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.docx', default_size, default_content)


class XLSXFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.xlsx', default_size, default_content)


class TXTFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.txt', default_size, default_content)

    def create_file(self, filename=None, size=None, content=None):
        """
        Override to handle text content encoding.
        """
        content = content.encode() if isinstance(content, str) else content or self.default_content
        super().create_file(filename, size, content)


class JPGFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.jpg', default_size, default_content)


class PNGFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.png', default_size, default_content)


class GIFFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.gif', default_size, default_content)


class ZIPFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.zip', default_size, default_content)


class TarFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.tar', default_size, default_content)


class Mp3FileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.mp3', default_size, default_content)


class WavFileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.wav', default_size, default_content)


class Mp4FileCreator(FileCreator):
    def __init__(self, default_size=1024, default_content=None):
        super().__init__('.mp4', default_size, default_content)


# Factory to get the appropriate FileCreator
class DummyFile:
    """
    A class to manage the creation out for various types of dummy files using the Template Pattern.
    """

    def __init__(self, default_size=1024, default_content=None):
        self.default_size = default_size
        self.default_content = default_content or b'0'
        self.created_files = []

        # Mapping extensions to their respective creators
        self.creators = {
            '.pdf': PDFFileCreator(default_size, default_content),
            '.epub': EPUBFileCreator(default_size, default_content),
            '.docx': DOCXFileCreator(default_size, default_content),
            '.xlsx': XLSXFileCreator(default_size, default_content),
            '.txt': TXTFileCreator(default_size, default_content),
            '.jpg': JPGFileCreator(default_size, default_content),
            '.png': PNGFileCreator(default_size, default_content),
            '.gif': GIFFileCreator(default_size, default_content),
            '.zip': ZIPFileCreator(default_size, default_content),
            # Add more creators as needed
        }

    def create_file(self, extension, filename=None, size=None, content=None):
        """
        Generic method to create a dummy file based on the extension.

        :param extension: File extension (e.g., '.pdf').
        :param filename: Name of the file to create.
        :param size: Size of the file in bytes.
        :param content: Content to fill the file.
        """
        creator = self.creators.get(extension)
        if not creator:
            print(f"No creator available for extension '{extension}'.")
            return
        creator.create_file(filename, size, content)
        self.created_files.extend(creator.created_files)

    def custom_file(self, filename, extension, header=None, size=None, content=None):
        """
        Create a custom dummy file.

        :param filename: Name of the file.
        :param extension: File extension (e.g., '.custom').
        :param header: Custom header bytes.
        :param size: Size of the file in bytes.
        :param content: Custom content to fill the file.
        """

        class CustomFileCreator(FileCreator):
            def get_header_inner(self):
                return header or self.FILE_HEADERS.get(extension, b'')

            def header(self):
                return self.get_header_inner()

            def default_filename(self):
                return filename

        custom_creator = CustomFileCreator(self.default_size, self.default_content)
        custom_creator.FILE_HEADERS[extension] = header or b''
        custom_creator.create_file(filename, size, content)
        self.created_files.extend(custom_creator.created_files)

    def reset(self):
        """
        Reset the list of created files.
        """
        self.created_files = []
        for creator in self.creators.values():
            creator.reset()
        print("Reset the list of created files.")

    @staticmethod
    def create_image(output_path):
        color = _random_color()
        img = Image.new('RGB', (100, 100), color=color)  # Create images with varying shades of red
        img.save(output_path)  # Save images as PNG files

    def create_video(self, output_path, sequence_dir=None, codec="libx264", fps=10):
        images = [file for file in os.listdir(sequence_dir) if is_image(os.path.join(sequence_dir, file))]
        temp_dir = os.path.join(os.getcwd(), "temp")

        if not images or sequence_dir is None:
            for i in range(10):
                path = os.path.join(temp_dir, f"image_{i:03d}.png")
                self.create_image(path)
                images.append(path)
        clip = ImageSequenceClip(images, fps=fps)
        clip.write_videofile(output_path, codec=codec)

        # Cleanup
        os.removedirs(temp_dir)

    @staticmethod
    def create_static_video(image_path, output_path, codec="libx264", duration=5):
        # Load the image and set its duration
        clip = ImageClip(image_path).set_duration(duration)
        clip.write_videofile(output_path, codec=codec)

    @staticmethod
    def create_audio(filename, duration=3000, frequency=440):
        # Generate a sine wave of specified frequency and duration (in milliseconds)
        audio = pydub.generators.Sine(frequency).to_audio_segment(duration=duration)
        # Export the audio to the specified format
        audio.export(filename, format=filename.split('.')[-1])

    def __repr__(self):
        total_files = sum(len(creator.created_files) for creator in self.creators.values())
        return f"<DummyFile created: {total_files} files>"

    def __str__(self):
        total_files = sum(len(creator.created_files) for creator in self.creators.values())
        return f"DummyFile Utility - {total_files} files created."


class LazyDescriptor:
    """Descriptor that implements lazy evaluation of class attributes."""

    def __init__(self, func: Callable[..., T]) -> None:
        self.func = func
        self.name = func.__name__
        self.cache_name = f'_lazy_{func.__name__}'

    def __get__(self, instance: Any, owner: Any) -> T:
        if instance is None:
            return self

        # Check if we've already computed and cached the value
        if not hasattr(instance, self.cache_name):
            # Compute and cache the value
            result = self.func(instance)
            setattr(instance, self.cache_name, result)

        return getattr(instance, self.cache_name)


def lazy_method(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator that makes a method or property lazy-evaluated.
    The result is computed only once and then cached.
    """
    if inspect.iscoroutinefunction(func):
        raise TypeError("Async functions are not supported")

    @wraps(func)
    def wrapped(self: Any, *args: Any, **kwargs: Any) -> T:
        cache_name = f'_lazy_{func.__name__}'

        if not hasattr(self, cache_name):
            result = func(self, *args, **kwargs)
            setattr(self, cache_name, result)

        return getattr(self, cache_name)

    return wrapped


class LazyMetaClass(type):
    """
    Metaclass that enables lazy evaluation of class attributes and methods.
    Methods decorated with @lazy_method will only be evaluated once when first accessed.
    """

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        # Transform methods marked with @lazy_method into LazyDescriptor instances
        for key, value in namespace.items():
            if hasattr(value, '_lazy'):
                namespace[key] = LazyDescriptor(value)

        return super().__new__(mcs, name, bases, namespace)


@dataclass
class FileMetadata:
    """Store metadata for recycled files."""
    original_path: str
    deletion_date: datetime
    size: int
    checksum: str
    tags: List[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary format."""
        return {
            'original_path': self.original_path,
            'deletion_date': self.deletion_date.isoformat(),
            'size': self.size,
            'checksum': self.checksum,
            'tags': self.tags or []
        }


class RecycleBinManager:
    """Singleton manager for recyclebin instances."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        self.bins: Dict[str, 'RecycleBin'] = {}
        self.max_bins = 5


class AbstractRecycleBin(ABC):
    """Abstract base class defining RecycleBin interface."""

    @abstractmethod
    def delete(self, path: str) -> None:
        """Move item to recycle bin."""
        pass

    @abstractmethod
    def restore(self, item_id: str) -> None:
        """Restore item from recycle bin."""
        pass


class RecycleBin(AbstractRecycleBin):
    """Advanced RecycleBin implementation with extensive features."""

    def __init__(self, location: str, max_size: int = 1024 * 1024 * 1024):
        """
        Initialize RecycleBin.

        Args:
            location: Base directory for the recycle bin
            max_size: Maximum size in bytes (default 1GB)
        """
        self.location = Path(location)
        self.max_size = max_size
        self.metadata_file = self.location / "metadata.json"
        self.items: Dict[str, FileMetadata] = {}
        self._lock = threading.RLock()
        self.logger = logging.getLogger(__name__)
        self._setup()

        # Thread pool for parallel operations
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        # Process pool for CPU-intensive operations
        self.process_pool = ProcessPoolExecutor(max_workers=2)

        # Queue for job handling
        self.job_queue = queue.PriorityQueue()
        self._start_job_handler()

    def _setup(self) -> None:
        """Initialize recycle bin directory structure."""
        self.location.mkdir(parents=True, exist_ok=True)
        if self.metadata_file.exists():
            self._load_metadata()

    def _load_metadata(self) -> None:
        """Load metadata from disk."""
        try:
            with open(self.metadata_file, 'r') as f:
                data = json.load(f)
                self.items = {
                    k: FileMetadata(
                        original_path=v['original_path'],
                        deletion_date=datetime.fromisoformat(v['deletion_date']),
                        size=v['size'],
                        checksum=v['checksum'],
                        tags=v['tags']
                    ) for k, v in data.items()
                }
        except Exception as e:
            self.logger.error(f"Failed to load metadata: {e}")
            self.items = {}

    def _save_metadata(self) -> None:
        """Save metadata to disk."""
        with self._lock:
            try:
                with open(self.metadata_file, 'w') as f:
                    json.dump({k: v.to_dict() for k, v in self.items.items()}, f)
            except Exception as e:
                self.logger.error(f"Failed to save metadata: {e}")

    def get_total_size(self) -> int:
        """Get total size of items in recycle bin."""
        return sum(item.size for item in self.items.values())

    def delete(self, path: str) -> str:
        """
        Move item to recycle bin.

        Args:
            path: Path to item to be deleted

        Returns:
            str: Item ID in recycle bin

        Raises:
            StorageFullError: If recycle bin is full
            FileNotFoundError: If item doesn't exist
        """
        with self._lock:
            path = Path(path)
            if not path.exists():
                raise FileNotFoundError(f"Item not found: {path}")

            size = path.stat().st_size if path.is_file() else sum(
                f.stat().st_size for f in path.rglob('*') if f.is_file()
            )
            total_size = self.get_total_size() + size
            if total_size > self.max_size:
                raise StorageFullError("Recycle bin storage limit exceeded")

            item_id = datetime.now().strftime('%Y%m%d_%H%M%S_') + path.name
            target = self.location / item_id

            try:
                shutil.move(str(path), str(target))
                metadata = FileMetadata(
                    original_path=str(path),
                    deletion_date=datetime.now(),
                    size=size,
                    checksum=self._calculate_checksum(target),
                    tags=[]
                )
                self.items[item_id] = metadata
                self._save_metadata()
                return item_id
            except Exception as e:
                self.logger.error(f"Failed to delete item: {e}")
                raise RecycleBinError(f"Failed to delete item: {e}")

    async def async_delete(self, path: str) -> str:
        """Asynchronous version of delete operation."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.thread_pool, self.delete, path)

    def restore(self, item_id: str) -> None:
        """
        Restore item from recycle bin.

        Args:
            item_id: ID of item to restore

        Raises:
            ItemNotFoundError: If item not found in recycle bin
            RestoreError: If restoration fails
        """
        with self._lock:
            if item_id not in self.items:
                raise ItemNotFoundError(f"Item not found: {item_id}")

            metadata = self.items[item_id]
            source = self.location / item_id
            target = Path(metadata.original_path)

            try:
                if target.exists():
                    raise RestoreError(f"Target path already exists: {target}")

                shutil.move(str(source), str(target))
                del self.items[item_id]
                self._save_metadata()
            except Exception as e:
                self.logger.error(f"Failed to restore item: {e}")
                raise RestoreError(f"Failed to restore item: {e}")

    async def async_restore(self, item_id: str) -> None:
        """Asynchronous version of restore operation."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self.thread_pool, self.restore, item_id)

    @staticmethod
    def _calculate_checksum(path: Path) -> str:
        """Calculate file checksum."""
        import hashlib
        hasher = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()

    def list_items(self, pattern: str = None) -> Generator[FileMetadata, None, None]:
        """List items in recycle bin with optional pattern matching."""
        for item_id, metadata in self.items.items():
            if not pattern or pattern in item_id:
                yield metadata

    def add_tag(self, item_id: str, tag: str) -> None:
        """Add tag to item."""
        with self._lock:
            if item_id not in self.items:
                raise ItemNotFoundError(f"Item not found: {item_id}")
            if self.items[item_id].tags is None:
                self.items[item_id].tags = []
            self.items[item_id].tags.append(tag)
            self._save_metadata()

    def remove_tag(self, item_id: str, tag: str) -> None:
        """Remove tag from item."""
        with self._lock:
            if item_id not in self.items:
                raise ItemNotFoundError(f"Item not found: {item_id}")
            if tag in self.items[item_id].tags:
                self.items[item_id].tags.remove(tag)
                self._save_metadata()

    def cleanup(self, days: int = 30) -> None:
        """Remove items older than specified days."""
        threshold = datetime.now() - timedelta(days=days)
        with self._lock:
            for item_id, metadata in list(self.items.items()):
                if metadata.deletion_date < threshold:
                    self._permanent_delete(item_id)

    def _permanent_delete(self, item_id: str) -> None:
        """Permanently delete item from recycle bin."""
        with self._lock:
            if item_id not in self.items:
                raise ItemNotFoundError(f"Item not found: {item_id}")

            path = self.location / item_id
            try:
                if path.is_file():
                    path.unlink()
                else:
                    shutil.rmtree(path)
                del self.items[item_id]
                self._save_metadata()
            except Exception as e:
                self.logger.error(f"Failed to permanently delete item: {e}")
                raise RecycleBinError(f"Failed to permanently delete item: {e}")

    def _start_job_handler(self) -> None:
        """Start background job handler thread."""

        def job_handler():
            while True:
                try:
                    priority, job = self.job_queue.get()
                    job()
                except Exception as e:
                    self.logger.error(f"Job handler error: {e}")
                finally:
                    self.job_queue.task_done()

        thread = threading.Thread(target=job_handler, daemon=True)
        thread.start()

    @contextmanager
    def batch_operation(self):
        """Context manager for batch operations."""
        try:
            with self._lock:
                yield
        finally:
            self._save_metadata()

    @asynccontextmanager
    async def async_batch_operation(self):
        """Async context manager for batch operations."""
        try:
            with self._lock:
                yield
        finally:
            self._save_metadata()

    def __str__(self) -> str:
        """String representation."""
        return f"RecycleBin(location='{self.location}', items={len(self.items)})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"RecycleBin(location='{self.location}', max_size={self.max_size}, items={len(self.items)})"

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)


if __name__ == "__main__":
    # Basic usage
    recyclebin = RecycleBin(".")
    item_id = recyclebin.delete("__init__.py")
    recyclebin.restore(item_id)

    # # Async usage
    # async with RecycleBin("/path/to/bin") as rb:
    #     item_id = await rb.async_delete("/path/to/file")
    #     await rb.async_restore(item_id)

    # Batch operations
    # with recyclebin.batch_operation():
    #     recyclebin.add_tag(item_id, "important")
    #     recyclebin.delete("/path/to/another/file")
    #
    # # List items with pattern
    # for item in recyclebin.list_items("*.txt"):
    #     print(item.original_path)
