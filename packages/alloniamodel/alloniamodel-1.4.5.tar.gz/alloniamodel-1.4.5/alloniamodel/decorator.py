from __future__ import annotations

import datetime
import inspect
import time
from copy import copy
from functools import wraps

from allonias3.helpers.class_property import classproperty
from typeguard import typechecked

from .checker import _check_attrs
from .errors import (
    NotReadyError,
    cannot_record_err,
    invalid_limit_arg_err,
    limit_arg_err,
)
from .utils import ExecutionList, ExecutionMetadata


class ReadyDecorator:
    """Decorate a class method with :obj:`ready` by specifying the
    optional *needed_attributes* argument, and by specyfing the
    :obj:`_always_check` class attributes at the beginning of your program
    through the :obj:`set_always_check` method.
    Then, each time the decorated method is run, :obj:`ready` will check that
    the specified attributes exist and are not None in the current instance of
    the method's class, and raise :obj:`~aleiamodel.errors.NotReadyError` if
    not.

    See Also:
        :obj:`~aleiamodel.errors.NotReadyError`
    """

    _always_check: tuple[str | tuple[str, str], ...] = ()
    """Can contain attribute names and/or pairs of (name, key).

    In the last case, will assume that the attribute *name* is a dictionary
    and will check that *key* is in it and not None. Those will be checked
    by :obj:`ready` for each run of any decorated method.

    :meta public:
    """

    @classproperty
    def always_check(cls) -> tuple[str | tuple[str, str], ...]:  # noqa: N805
        return cls._always_check

    @classmethod
    @typechecked
    def set_always_check(cls, value: tuple[str | tuple[str, str], ...]):
        """Changes :obj:`_always_check` to the given value."""
        cls._always_check = value

    @classmethod
    @typechecked
    def ready(cls, needed_attributes: tuple[str | tuple[str, str], ...]):
        """Decorate a class method with it, the decorator will check that the
        class attributes are defined and not None before executing the method.

        Args:
            needed_attributes: Can contain attribute names and/or pairs of
                (name, key). In the last case, will assume that the attribute
                *name* is a dictionary and will check that *key* is in it and
                not None. Can also contain 'attr1 | (attr2, key) | ...', where
                only one of the given attrs will be needed. Does not support
                XOR.

        Raises:
            :obj:`~aleiamodel.errors.NotReadyError`
        """

        def decorator_ready(func):
            @wraps(func)
            def wrapper(obj, *args, **kwargs):
                if (missing_attrs := _check_attrs(obj, cls.always_check)) or (
                    missing_attrs := _check_attrs(obj, needed_attributes)
                ):
                    raise NotReadyError(func.__qualname__, missing_attrs)
                return func(obj, *args, **kwargs)

            return wrapper

        return decorator_ready


@typechecked
def _record_execution(
    to_attribute: str, record_results: bool, raise_error: bool = True
):
    """Decorate a class method with it to record the execution time, duration,
    used kwargs, and optionaly results of the method each time it is
    called.

    Can not be used on static methods, as the decorator needs access to the
    object to record the metadata.
    """

    def decorator_record_execution(func):
        @wraps(func)
        def wrapper(obj, *args, **kwargs):
            now = datetime.datetime.now()
            t0 = time.time()
            skip_update = kwargs.pop("__skip_description_update", False)
            if raise_error is True:
                result = func(obj, *args, **kwargs)
                record_results_ = record_results
                model = result["model"]
                dataset_revision = result["dataset_revision"]
                to_ret = result["results"]
                result = to_ret
            else:
                try:
                    result = func(obj, *args, **kwargs)
                    record_results_ = record_results
                    model = result["model"]
                    dataset_revision = result["dataset_revision"]
                    to_ret = result["results"]
                    result = to_ret
                except Exception as e:
                    to_ret = e
                    result = f"{e.__class__.__name__}: {e}"
                    model = None
                    dataset_revision = None
                    record_results_ = True
            t1 = time.time()

            attribute = getattr(obj, to_attribute, ExecutionList(obj))
            if not isinstance(attribute, ExecutionList):
                raise cannot_record_err(to_attribute, type(attribute))
            attribute.append(
                ExecutionMetadata(
                    dataset_revision=dataset_revision,
                    model=model,
                    date=now,
                    duration=round((t1 - t0), 3),  # in s
                    parameters=kwargs,
                    results=copy(result) if record_results_ else None,
                )
            )
            # set attribute to trigger any overloaded __setattr__. In
            # AleiaModel for instance, it might update the model's description
            # depending on the updated attribute.
            if not skip_update:
                setattr(obj, to_attribute, attribute)
            return to_ret

        return wrapper

    return decorator_record_execution


@typechecked
def _limit_arguments(
    number_of_args: int | None = None,
    min_args: int | None = None,
    max_args: int | None = None,
):
    """Decorate a setter for a property of a callable with it.

    Assuming the argument of the setter is a callable, checkes that this
    callable has the right number of arguments.

    Args:
        number_of_args: Can not be given alongside *min_* or *max_*. Enforces
            the number of acceptable arguments to exactly this value.
        min_args: Can not be given alongside *n*. Enforces the number of
            acceptable arguments to at least this value.
        max_args: Can not be given alongside *n*. Enforces the number of
            acceptable arguments to at most this value.

    Raises:
        ValueError: If :inlinepython:`n` is given alongside :inlinepython:`min_`
            :inlinepython:`max_` or the opposite, if :inlinepython:`min_`
            is greater than :inlinepython:`max_`, if the number of
            arguments accepted by the callable does not match the specified
            limits.
    """
    if number_of_args is not None and (
        min_args is not None or max_args is not None
    ):
        raise invalid_limit_arg_err("one")
    if number_of_args is None and min_args is None and max_args is None:
        raise invalid_limit_arg_err("none")
    if min_args is not None and max_args is not None and min_args > max_args:
        raise invalid_limit_arg_err("all")

    def decorator_limit_arguments(func):
        @wraps(func)
        def wrapper(obj, *args, **kwargs):
            func_to_limit = args[0]
            nargs = len(inspect.signature(func_to_limit).parameters)
            if number_of_args is not None and nargs != number_of_args:
                raise limit_arg_err(nargs, number_of_args=number_of_args)
            if min_args is not None and nargs < min_args:
                raise limit_arg_err(nargs, min_args=min_args)
            if max_args is not None and nargs > max_args:
                raise limit_arg_err(nargs, max_args=max_args)
            return func(obj, *args, **kwargs)

        return wrapper

    return decorator_limit_arguments


def convert_self_kwarg(func):
    """Will look for :inlinepython:`"self"` in the keyword arguments' values
    given to the decorated method and replace it by the first argument of the
    function, which should correspond to the object the method belongs to
    (i.e, 'self')."""

    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        # Check instance first, because doing value != "self" on a NumPy array
        # or Pandas DataFrame has strange behavior.
        kwargs = {
            key: value if not isinstance(value, str) or value != "self" else obj
            for key, value in kwargs.items()
        }
        return func(obj, *args, **kwargs)

    return wrapper
