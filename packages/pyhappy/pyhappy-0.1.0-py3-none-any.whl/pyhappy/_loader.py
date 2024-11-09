import importlib.util
import threading
from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Optional, Type, Union

from pyhappy.exceptions import PluginNotFoundError, LoaderError


class BasePlugin(ABC):
    """Abstract base class for plugins"""

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin"""
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute the plugin's main functionality"""
        pass


class Loader:
    """
    A thread-safe dynamic loader class for plugins and modules
    with support for hot-reloading and dependency management.
    """

    def __init__(self, plugin_directory: Union[str, Path]):
        self._plugin_dir = Path(plugin_directory)
        self._loaded_plugins: Dict[str, Type[BasePlugin]] = {}
        self._lock = threading.RLock()
        self._plugin_instances: Dict[str, BasePlugin] = {}
        self._watch_thread: Optional[threading.Thread] = None
        self._should_watch = threading.Event()

    def __repr__(self) -> str:
        return f"Loader(plugin_directory='{self._plugin_dir}')"

    def __str__(self) -> str:
        return f"Plugin Loader with {len(self._loaded_plugins)} plugins loaded"

    @contextmanager
    def plugin_session(self, plugin_name: str) -> BasePlugin:
        """Context manager for temporary plugin usage"""
        plugin = self.load_plugin(plugin_name)
        try:
            yield plugin
        finally:
            self.unload_plugin(plugin_name)

    def load_plugin(self, plugin_name: str) -> BasePlugin:
        """Load and initialize a plugin by name"""
        with self._lock:
            if plugin_name in self._plugin_instances:
                return self._plugin_instances[plugin_name]

            try:
                plugin_path = self._plugin_dir / f"{plugin_name}.py"
                if not plugin_path.exists():
                    raise PluginNotFoundError(f"Plugin {plugin_name} not found")

                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                if spec is None or spec.loader is None:
                    raise LoaderError(f"Failed to create spec for plugin {plugin_name}")

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                plugin_class = getattr(module, plugin_name)
                if not issubclass(plugin_class, BasePlugin):
                    raise LoaderError(f"{plugin_name} is not a valid Plugin class")

                plugin_instance = plugin_class()
                plugin_instance.initialize()
                self._plugin_instances[plugin_name] = plugin_instance
                return plugin_instance

            except Exception as e:
                raise LoaderError(f"Failed to load plugin {plugin_name}: {str(e)}")

    def unload_plugin(self, plugin_name: str) -> None:
        """Unload a plugin"""
        with self._lock:
            self._plugin_instances.pop(plugin_name, None)

    def start_watching(self) -> None:
        """Start watching for plugin changes"""
        if self._watch_thread is None:
            self._should_watch.set()
            self._watch_thread = threading.Thread(target=self._watch_for_changes)
            self._watch_thread.daemon = True
            self._watch_thread.start()

    def stop_watching(self) -> None:
        """Stop watching for plugin changes"""
        if self._watch_thread is not None:
            self._should_watch.clear()
            self._watch_thread.join()
            self._watch_thread = None

    def _watch_for_changes(self) -> None:
        """Watch for changes in plugin files and reload as necessary"""
        last_modified: Dict[str, float] = {}
        while self._should_watch.is_set():
            for plugin_file in self._plugin_dir.glob("*.py"):
                mtime = plugin_file.stat().st_mtime
                if plugin_file.stem in last_modified:
                    if mtime > last_modified[plugin_file.stem]:
                        self.unload_plugin(plugin_file.stem)
                        try:
                            self.load_plugin(plugin_file.stem)
                        except Exception as e:
                            raise LoaderError(f"Failed to load plugin {plugin_file.stem}: {str(e)}")
                last_modified[plugin_file.stem] = mtime
            threading.Event().wait(1.0)
