"""
Module for utility functions, decorators, and context managers.

This module provides a variety of utility functions and decorators aimed at enhancing
the robustness, flexibility, and functionality of Python applications. It includes
tools for debugging, profiling, caching, managing logging levels, multithreading,
singleton pattern implementation, exception handling, and more.

Key functionalities:
- Console Output Control: Functions to enable or suppress console output.
- Type Checkers: Functions to check types such as iterables, iterators, and generators.
- Decorators: Includes decorators for retrying functions, exception handling,
  profiling, caching (memoization), singleton pattern, and execution limiting.
- Context Managers: Tools for temporarily changing log levels and suppressing warnings.
- Multithreading: Utilities for running functions concurrently with thread pools.
- Network Check: Function to verify internet connectivity by attempting to reach a URL.

The module also includes examples of custom exception classes for advanced error handling
and a Singleton metaclass for enforcing single-instance patterns.

Typical Use Cases:
- Utility for various data type checks and manipulations.
- Application performance profiling and debugging.
- Enhanced logging control for modules that require temporary or dynamic logging levels.
- Simplified multithreading operations with thread pool management.
- Network connectivity validation within the application.

Example:
    ```
    # Suppress console printing
    stop_console_printing()

    # Enable profiling on a function
    @profile
    def compute():
        pass
    ```

This module is especially useful for developers needing optimized control over
debugging, performance measurement, and singleton enforcement.
"""

from __future__ import annotations

import asyncio
import builtins
import cProfile
import contextlib
import functools
import inspect
import logging
import os
import pstats
import sys
import threading
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from functools import wraps
from operator import pow, add, sub, truediv, floordiv, mod, mul
from typing import Optional, Dict, Any
from typing import ParamSpec
from typing import (Type, Iterable, Iterator, Generator, Never)
from typing import TypeVar, Generic, Callable, Awaitable, Union, Coroutine
from urllib.error import URLError
from urllib.request import urlopen

from pyhappy.exceptions import BreakerThresholdError, UnificationError

T = TypeVar("T")
R = TypeVar('R')
P = ParamSpec("P")


def stop_console_printing(include_stderr: bool = False):
    if include_stderr:
        warnings.warn("This is not recommended. Please use this on your own risk.", stacklevel=2)
        sys.stderr = open(os.devnull, 'w')
    sys.stdout = open(os.devnull, 'w')


def start_console_printing():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def is_iterable(x: Any) -> bool:
    return isinstance(x, Iterable)


def is_iterator(x: Any) -> bool:
    return isinstance(x, Iterator)


def is_generator(x: Any) -> bool:
    return isinstance(x, Generator)


# noinspection PyUnusedLocal
def empty_function(func: Never):
    pass


def stop_print():
    builtins.print = empty_function


def start_print():
    builtins.print = print


def null_decorator():
    """
    A decorator returns null
    :return:
    """
    return None


@contextlib.contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


def trace(func: Callable) -> Callable:
    functools.wraps(func)

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) ' f'-> {result!r}')
        return result

    return wrapper


def get_module_size(module):
    size = 0
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        size += sys.getsizeof(attr)
    return size


def raised_exception(exception: Type[Exception]) -> Callable:
    """
    A decorator that transforms any exception from the decorated function into the specified exception type.

    Args:
        exception: The exception type to raise

    Returns:
        Callable: A decorator function
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise exception from e

        return wrapper

    return decorator


def find_path(node: str, cwd: str = ".") -> Optional[str]:
    """Search for a file 'node' starting from the directory 'cwd'."""
    for root, dirs, files in os.walk(cwd):
        if node in files:
            return os.path.join(root, node)
    return None


def is_hashable(value: T) -> bool:
    """Check if a value is hashable."""
    try:
        hash(value)
        return True
    except TypeError:
        return False


def is_mutable(value: T) -> bool:
    """Check if a value is mutable."""
    return isinstance(value, (list, dict, set, bytearray))


def profile(func: Callable) -> Callable:
    """Simple profiling wrapper using 'cProfile'."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumtime')
        stats.print_stats()  # You can print or save the stats
        return result

    return wrapper


def simple_debugger(func):
    def wrapper(*args, **kwargs):
        # print the function name and arguments
        print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
        # call the function
        result = func(*args, **kwargs)
        # print the results
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


def retry(exception: Type[Exception] = Exception, max_attempts: int = 5, delay: int = 1) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    if attempt == max_attempts:
                        print(f"Function failed after {max_attempts} attempts")
                        raise e
                    print(f"Attempt {attempt} failed. Retrying in {delay} seconds...")
                    time.sleep(delay)

        return wrapper

    return decorator


# Exception Handler
def simple_exception(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An exception occurred: {e}")
            raise

    return wrapper


def make_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # If the first argument is a function, assume we're being used as a decorator
        if len(args) == 1 and callable(args[0]):
            def decorated(target_func):
                @functools.wraps(target_func)
                def new_func(*func_args, **func_kwargs):
                    return func(target_func, *func_args, **func_kwargs)

                return new_func

            return decorated(args[0])
        else:
            # Otherwise, run the function normally
            return func(*args, **kwargs)

    return wrapper


def memoize(func: Callable[P, T]) -> Callable[P, T]:
    cache: Dict[str, T] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        key = _generate_cache_key(func, args, kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


# Helper to generate a cache key for memoization
def _generate_cache_key(func: Callable, args: tuple, kwargs: dict) -> str:
    key = (
        f"{func.__name__}({', '.join(map(repr, args))}"
        f"{', ' if args and kwargs else ''}"
        f"{', '.join(f'{k}={v!r}' for k, v in kwargs.items())})"
    )
    return key


def is_decorator(func):
    # Check if the function itself is callable
    if not callable(func):
        return False

    # Define a sample function to pass to the decorator
    sample_func = lambda: None

    # Use `inspect` to get the function signature
    signature = inspect.signature(func)
    parameters = list(signature.parameters.values())

    # Check if the function takes exactly one parameter
    if len(parameters) != 1:
        return False

    # The parameter should not have a default value (should always be passed)
    param = parameters[0]
    if param.default != inspect.Parameter.empty:
        return False

    # The parameter should accept a callable (function)
    if param.annotation not in (inspect.Parameter.empty, callable):
        if param.annotation and not callable(param.annotation):
            return False

    # Try calling the function with a sample callable to check if it acts as a decorator
    with contextlib.suppress(Exception):
        result = func(sample_func)
        # If the result is callable, it confirms the function is a decorator
        return callable(result)

    return False


def run_once(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)
        return None

    wrapper.has_run = False
    return wrapper


def monitor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logging.info(f"Function {func.__name__} executed successfully in {elapsed_time:.4f} seconds.")
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logging.error(f"Function {func.__name__} failed after {elapsed_time:.4f} seconds with error: {e}")
            raise

    return wrapper


def multithreaded(max_workers: int = 5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_args = {executor.submit(func, arg): arg for arg in args[0]}
                return _collect_multithreaded_results(future_to_args)

        return wrapper

    return decorator


# Helper to collect results from multithreaded execution
def _collect_multithreaded_results(future_to_args: dict) -> list:
    results = []
    for future in as_completed(future_to_args):
        arg = future_to_args[future]
        try:
            result = future.result()
        except Exception as exc:
            print(f'{arg} generated an exception: {exc}')
        else:
            results.append(result)
    return results


@contextlib.contextmanager
def ignore_warnings():
    """Context manager to ignore warning within the 'with' statement."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield


# Check Internet Connectivity
def check_internet_connectivity(url: str) -> None:
    try:
        protocols = ["https://", "http://"]
        if not any(proto in url for proto in protocols):
            url = "https://" + url
        urlopen(url, timeout=2)
        print(f'Connection to "{url}" is working')
    except URLError as e:
        raise URLError(f"Connection error: {e.reason}")


def singleton(cls):
    __instance = None
    __lock = threading.Lock()

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal __instance
        with __lock:
            if __instance is None:
                __instance = cls(*args, **kwargs)
        return __instance

    return wrapper


# Breaker Decorator
def breaker(threshold):
    """A decorator that breaks a function once a specified threshold is reached (e.g., number of calls)."""

    def decorator(func):
        func.counter = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.counter >= threshold:
                raise BreakerThresholdError(f"Function '{func.__name__}' reached the threshold of {threshold} calls")

            result = func(*args, **kwargs)
            func.counter += 1
            return result

        return wrapper

    return decorator


class SingletonMeta(type):
    """
    A thread-safe implementation of Singleton using metaclasses.
    """
    __instances = {}
    __lock: threading.Lock = threading.Lock()
    __slots__ = ()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                instance = super().__call__(*args, **kwargs)
                cls.__instances[cls] = instance
        return cls.__instances[cls]

    @property
    def instance(cls):
        return cls.__instances[cls]


def safe(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ArithmeticError:
            return NotImplemented

    return wrapper


@safe
def _do_arithmatic(self, other, op, derived_op):
    op_result = getattr(type(self), derived_op)(self, other)
    if op_result is NotImplemented:
        return op_result
    return op(self.value, other.value)


# def _do_arithmatic(classes: Tuple[T, T], values: Tuple[Any, Any], op, derived_op):
#     self, other = classes
#     self_value, other_value = values
#     op_result = getattr(type(self), derived_op)(self, other)
#     if op_result is NotImplemented:
#         return op_result
#     return op(self_value, other_value)


class FixIDEComplain:
    """A mixin class to fix IDE complaints about dynamically added methods, with on-demand generation."""

    def __getattr__(self, name):
        """Generate missing operators dynamically."""
        if name in _convert:
            # Generate the dynamic method on-the-fly using the _convert dictionary
            for opname, opfunc in _convert[name]:
                setattr(self, opname, opfunc)
            # Once generated, return the first operation function
            return getattr(self, name)
        raise AttributeError(f"{type(self).__name__} object has no attribute '{name}'")


def _sub_from_add(self, other):
    return _do_arithmatic(self, other, sub, '__add__')


def _floordiv_from_add(self, other):
    return _do_arithmatic(self, other, floordiv, '__add__')


def _truediv_from_add(self, other):
    return _do_arithmatic(self, other, truediv, '__add__')


def _mul_from_add(self, other):
    return _do_arithmatic(self, other, mul, '__add__')


def _mod_from_add(self, other):
    return _do_arithmatic(self, other, mod, '__add__')


def _pow_from_add(self, other):
    return _do_arithmatic(self, other, pow, '__add__')


def _iadd_from_add(self, other):
    result = self + other
    if result is NotImplemented:
        return NotImplemented
    self.value = result.value
    return self


def _radd_from_add(self, other):
    return type(self)(other + self.value)


def _floordiv_from_truediv(self, other):
    return _do_arithmatic(self, other, floordiv, '__truediv__')


def _add_from_truediv(self, other):
    return _do_arithmatic(self, other, add, '__truediv__')


def _mul_from_truediv(self, other):
    return _do_arithmatic(self, other, mul, '__truediv__')


def _mod_from_truediv(self, other):
    return _do_arithmatic(self, other, mod, '__truediv__')


def _pow_from_truediv(self, other):
    return _do_arithmatic(self, other, pow, '__truediv__')


def _sub_from_truediv(self, other):
    return _do_arithmatic(self, other, sub, '__truediv__')


def _itruediv_from_truediv(self, other):
    op_result = type(self).__truediv__(self, other)
    if op_result is NotImplemented:
        return NotImplemented
    self.value /= op_result
    return self


def _rtruediv_from_truediv(self, other):
    return type(self)(other / self.value)


def _add_from_sub(self, other):
    return _do_arithmatic(self, other, add, '__sub__')


def _mul_from_sub(self, other):
    return _do_arithmatic(self, other, mul, '__sub__')


def _truediv_from_sub(self, other):
    return _do_arithmatic(self, other, truediv, '__sub__')


def _floordiv_from_sub(self, other):
    return _do_arithmatic(self, other, floordiv, '__sub__')


def _mod_from_sub(self, other):
    return _do_arithmatic(self, other, mod, '__sub__')


def _pow_from_sub(self, other):
    return _do_arithmatic(self, other, pow, '__sub__')


def _isub_from_sub(self, other):
    op_result = type(self).__sub__(self, other)
    if op_result is NotImplemented:
        return NotImplemented
    self.value -= op_result
    return self


def _rsub_from_sub(self, other):
    return type(self)(other - self.value)


def _add_from_mul(self, other):
    return _do_arithmatic(self, other, add, '__mul__')


def _truediv_from_mul(self, other):
    return _do_arithmatic(self, other, truediv, '__mul__')


def _sub_from_mul(self, other):
    return _do_arithmatic(self, other, sub, '__mul__')


def _pow_from_mul(self, other):
    return _do_arithmatic(self, other, pow, '__mul__')


def _floordiv_from_mul(self, other):
    return _do_arithmatic(self, other, floordiv, '__mul__')


def _mod_from_mul(self, other):
    return _do_arithmatic(self, other, mod, '__mul__')


def _imul_from_mul(self, other):
    op_result = type(self).__mul__(self, other)
    if op_result is NotImplemented:
        return NotImplemented
    self.value *= op_result
    return self


def _rmul_from_mul(self, other):
    return type(self)(other + self.value)


_convert = {
    '__add__': [
        ('__sub__', _sub_from_add),
        ('__iadd__', _iadd_from_add),
        ('__radd__', _radd_from_add),
        ('__mul__', _mul_from_add),
        ('__truediv__', _truediv_from_add),
        ('__floordiv__', _floordiv_from_add),
        ('__mod__', _mod_from_add),
        ('__pow__', _pow_from_add)
    ],
    '__sub__': [
        ('__add__', _add_from_sub),
        ('__isub__', _isub_from_sub),
        ('__radd__', _rsub_from_sub),
        ('__mul__', _mul_from_sub),
        ('__truediv__', _truediv_from_sub),
        ('__floordiv__', _floordiv_from_sub),
        ('__mod__', _mod_from_sub),
        ('__pow__', _pow_from_sub)
    ],
    '__mul__': [
        ('__add__', _add_from_mul),
        ('__sub__', _sub_from_mul),
        ('__imul__', _imul_from_mul),
        ('__rmul__', _rmul_from_mul),
        ('__truediv__', _truediv_from_mul),
        ('__floordiv__', _floordiv_from_mul),
        ('__mod__', _mod_from_mul),
        ('__pow__', _pow_from_mul)
    ],
    '__truediv__': [
        ('__add__', _add_from_truediv),
        ('__sub__', _sub_from_truediv),
        ('__floordiv__', _floordiv_from_truediv),
        ('__mul__', _mul_from_truediv),
        ('__itruediv__', _itruediv_from_truediv),
        ('__rtruediv__', _rtruediv_from_truediv),
        ('__mod__', _mod_from_truediv),
        ('__pow__', _pow_from_truediv)
    ],
    # ...
}


def arithmatic_total_ordering(cls):
    """Class decorator that fills in missing ordering methods"""
    # Find which ordering operation(s) are defined
    roots = {op for op in _convert if getattr(cls, op, None) is not getattr(object, op, None)}
    if not roots:
        raise ValueError('must define at least one ordering operation: + - * /')

    # Add all related operations based on defined ones
    for root in roots:
        for opname, opfunc in _convert[root]:
            if opname not in roots:
                opfunc.__name__ = opname
                setattr(cls, opname, opfunc)
    return cls


class UnifiedOperation(Generic[P, R]):
    """
    A descriptor that handles both sync and async operations transparently.
    The actual implementation is chosen based on the caller's context.
    """

    def __init__(
            self,
            sync_impl: Callable[P, R],
            async_impl: Callable[P, Awaitable[R]]
    ):
        self.sync_impl = sync_impl
        self.async_impl = async_impl

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        @wraps(self.sync_impl)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Union[R, Awaitable[R]]:
            # Check if we're in an async context
            try:
                asyncio.get_running_loop()
                is_async = True
            except RuntimeError:
                is_async = False

            if is_async:
                return self.async_impl(*args, **kwargs)
            return self.sync_impl(*args, **kwargs)

        return wrapper

    def __call__(self, *args, **kwargs):
        raise UnificationError("Cant unify dynamic methods, have you inherited from 'DynamicUnifiedOperation'")

    def __await__(self):
        raise UnificationError("Cant unify dynamic methods, have you inherited from 'DynamicUnifiedOperation'")


class DynamicUnifiedOperation:
    """A class to hold dynamically created unified operations"""

    def __init__(self):
        self._operations = {}

    def __setattr__(self, name: str, value: UnifiedOperation):
        if isinstance(value, UnifiedOperation):
            # Store the operation's implementation
            self._operations[name] = value.__get__(self)
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name: str):
        if name in getattr(self, '_operations', {}):
            return self._operations[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


def create_unified_operation(
        sync_fn: Callable[P, R],
        async_fn: Callable[P, Awaitable[R]]
) -> UnifiedOperation[P, R]:
    """
    Helper method to create unified operations with proper type hints
    """
    if not (isinstance(sync_fn, Callable) and isinstance(async_fn, Callable)) or isinstance(async_fn, Coroutine):
        raise ValueError("Both sync_fn and async_fn must be callable, and async_fn must be a coroutine function")
    return UnifiedOperation(sync_fn, async_fn)


@functools.total_ordering
@dataclass(frozen=True, kw_only=True)
class Constants:
    def __init__(self, **kwargs):
        self.__initialize_constants(**kwargs)

    def __initialize_constants(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Constants) and self.__dict__ == other.__dict__

    def __lt__(self, other):
        if not isinstance(other, Constants):
            return NotImplemented
        return tuple(sorted(self.__dict__.items())) < tuple(sorted(other.__dict__.items()))


@functools.total_ordering
class Pointer:
    def __init__(self, value=None):
        """Initialize the pointer with a value."""
        self._value = [value]  # Use a list to hold the reference

    @property
    def value(self):
        return self.get()

    def get(self):
        """Dereference the pointer to access the value."""
        return self._value[0]

    def set(self, value):
        """Dereference the pointer and set the new value."""
        self._value[0] = value

    def address(self):
        """Return the 'address' of the pointer, which in this case is its own id."""
        return id(self._value)

    def point_to(self, other_pointer):
        """Point this pointer to the memory location of another pointer."""
        if isinstance(other_pointer, Pointer):
            self._value = other_pointer._value
        else:
            raise TypeError("point_to expects another Pointer instance")

    def is_null(self):
        """Check if the pointer is null (i.e., points to None)."""
        return self._value[0] is None

    def __str__(self):
        """String representation showing the value and the 'address'."""
        return f"{self.__class__.__name__}(value={self._value[0]}, address={self.address()})"

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        self._value[0] = None

    def __lt__(self, other):
        if not isinstance(other, Pointer):
            return NotImplemented
        return self.get() < other.get()
