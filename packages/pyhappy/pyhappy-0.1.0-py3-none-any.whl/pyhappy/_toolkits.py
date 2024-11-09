from __future__ import annotations

import inspect
import threading
from functools import wraps
from typing import Any
from typing import (Type)

from pyhappy.exceptions import ProtectedAccessError, PrivateAccessError, InvalidInheritanceError


# Private Decorator
def private(cls_or_func):
    """A decorator that hides the class or method's attributes and methods, preventing outside access."""

    def class_decorator(cls):
        original_dict = cls.__dict__.copy()

        def new_getattribute(self, name):
            if name.startswith('_') and not name.startswith('__'):
                raise PrivateAccessError(f"Cannot access private attribute '{name}'")
            return object.__getattribute__(self, name)

        cls.__getattribute__ = new_getattribute

        for key in list(original_dict.keys()):
            if key.startswith('_') and not key.startswith('__'):
                delattr(cls, key)

        return cls

    if isinstance(cls_or_func, type):
        return class_decorator(cls_or_func)

    @wraps(cls_or_func)
    def function_decorator(*args, **kwargs):
        if cls_or_func.__name__.startswith('_'):
            raise PrivateAccessError(f"Cannot access private function '{cls_or_func.__name__}'")
        return cls_or_func(*args, **kwargs)

    return function_decorator


# Protected Decorator
def protect(cls_or_func):
    """A decorator that allows access to methods or attributes only for subclasses."""

    def class_decorator(cls):
        def new_getattribute(self, name):
            if name.startswith('_') and not isinstance(self, cls.__class__):
                raise ProtectedAccessError(f"Cannot access protected attribute '{name}'")
            return object.__getattribute__(self, name)

        cls.__getattribute__ = new_getattribute
        return cls

    if isinstance(cls_or_func, type):
        return class_decorator(cls_or_func)

    @wraps(cls_or_func)
    def function_decorator(*args, **kwargs):
        if cls_or_func.__name__.startswith('_'):
            raise ProtectedAccessError(f"Cannot access protected function '{cls_or_func.__name__}'")
        return cls_or_func(*args, **kwargs)

    return function_decorator


class AccessControlRegistry:
    """Thread-safe registry for tracking class access information."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._protected_access_registry = set()
                cls._instance._private_access_registry = {}
        return cls._instance

    def register_protected_access(self, module_name: str) -> None:
        """Register a module for protected access."""
        with self._lock:
            self._protected_access_registry.add(module_name)

    def register_private_access(self, class_name: str, allowed_scope: str) -> None:
        """Register a class and its allowed scope for private access."""
        with self._lock:
            self._private_access_registry[class_name] = allowed_scope

    def is_protected_access_allowed(self, module_name: str) -> bool:
        """Check if protected access is allowed for the given module."""
        return module_name in self._protected_access_registry

    def is_private_access_allowed(self, class_name: str, scope: str) -> bool:
        """Check if private access is allowed for the given class and scope."""
        return (class_name in self._private_access_registry and
                self._private_access_registry[class_name] == scope)


class PrivateClassMeta(type):
    """
    A thread-safe implementation of Private class behavior using metaclasses.

    This metaclass ensures that:
    1. The class cannot be inherited
    2. The class can only be accessed within the module it's defined in
    3. Provides proper attribute access control

    Example:
        ```python
        class MyPrivateClass(metaclass=PrivateClassMeta):
            def __init__(self):
                self._private_data = "sensitive"
        ```
    """
    _registry = AccessControlRegistry()

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Type:
        # Check for inheritance violation
        if bases != (object,):
            raise InvalidInheritanceError(
                f"Cannot inherit from private class {name}. Private classes cannot be inherited."
            )

        # Get the module where the class is being defined
        frame = inspect.currentframe().f_back
        defining_module = frame.f_globals['__name__']

        # Register the class in the registry
        mcs._registry.register_private_access(name, defining_module)

        # Add module information to the class
        namespace['_defining_module'] = defining_module

        return super().__new__(mcs, name, bases, namespace)

    def __call__(cls, *args, **kwargs) -> Any:
        # Check access permission during instantiation
        frame = inspect.currentframe().f_back
        calling_module = frame.f_globals['__name__']

        if not cls._registry.is_private_access_allowed(cls.__name__, calling_module):
            raise PrivateAccessError(
                f"Cannot access private class {cls.__name__} from module {calling_module}"
            )

        instance = super().__call__(*args, **kwargs)
        return instance

    def __str__(cls) -> str:
        return f"Private class '{cls.__name__}' defined in module '{cls._defining_module}'"

    def __repr__(cls) -> str:
        return f"<PrivateClass {cls.__name__} at {hex(id(cls))} defined in {cls._defining_module}>"


class ProtectedClassMeta(type):
    """
    A thread-safe implementation of Protected class behavior using metaclasses.

    This metaclass ensures that:
    1. The class can only be accessed within its own module or by subclasses
    2. Provides proper attribute access control
    3. Maintains inheritance hierarchy information

    Example:
        ```python
        class MyProtectedClass(metaclass=ProtectedClassMeta):
            def __init__(self):
                self._protected_data = "internal"
        ```
    """
    _registry = AccessControlRegistry()

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Type:
        # Get the module where the class is being defined
        frame = inspect.currentframe().f_back
        defining_module = frame.f_globals['__name__']

        # Register the module in the registry
        mcs._registry.register_protected_access(defining_module)

        # Add module information to the class
        namespace['_defining_module'] = defining_module
        namespace['_derived_modules'] = set()

        # Track inheritance information
        for base in bases:
            if hasattr(base, '_derived_modules'):
                base._derived_modules.add(defining_module)

        return super().__new__(mcs, name, bases, namespace)

    def __call__(cls, *args, **kwargs) -> Any:
        # Check access permission during instantiation
        frame = inspect.currentframe().f_back
        calling_module = frame.f_globals['__name__']

        if not (cls._registry.is_protected_access_allowed(calling_module) or
                calling_module in cls._derived_modules):
            raise ProtectedAccessError(
                f"Cannot access protected class {cls.__name__} from module {calling_module}"
            )

        instance = super().__call__(*args, **kwargs)
        return instance

    def __str__(cls) -> str:
        derived = ", ".join(cls._derived_modules) if cls._derived_modules else "None"
        return (f"Protected class '{cls.__name__}' defined in module '{cls._defining_module}' "
                f"with derived modules: {derived}")

    def __repr__(cls) -> str:
        return (f"<ProtectedClass {cls.__name__} at {hex(id(cls))} "
                f"defined in {cls._defining_module}>")


# Decorator for protected methods
def protected_method(func):
    """
    Decorator to enforce protected method access control.
    Only allows access from within the same module or derived classes.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        frame = inspect.currentframe().f_back
        calling_module = frame.f_globals['__name__']

        if not hasattr(args[0], '_defining_module'):
            raise ProtectedAccessError("Protected method decorator can only be used with protected classes")

        instance = args[0]
        defining_module = instance._defining_module

        if (calling_module != defining_module and
                calling_module not in getattr(instance.__class__, '_derived_modules', set())):
            raise ProtectedAccessError(
                f"Cannot access protected method {func.__name__} from module {calling_module}"
            )

        return func(*args, **kwargs)

    return wrapper
