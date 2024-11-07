from __future__ import annotations

import re

from .errors import invalid_kwargs_err
from .utils import check_attrs_filter, check_attrs_to_keep


def _check_attrs(  # noqa: PLR0912
    obj, attrs: tuple[str | tuple[str, str], ...]
) -> list[str]:
    """Checks that the given attributes ('attrs') exist and are not None in the
    given object ('obj').

    Args:
        attrs: Can contain attribute names and/or pairs of (name, key). In the
            last case, will assume that the attribute 'name' is a dictionary
            and will check that 'key' is in it and not None. Can also
            contain 'attr1 | (attr2, key) | ...', where only one of the given
            attrs will be needed. Does not support XOR.

    Returns:
        The list of attributes that do not exist or are None.

    Raises:
        ValueError: If any member of *attrs* is not understood.
    """
    bad_attrs = []
    for attr in attrs:
        if isinstance(attr, str) and "|" in attr:
            bad_attr = attr
            for attr_ in attr.split("|"):
                # OR is used: Stop if at least one attribute is good
                if len(_check_attrs(obj, (attr_.strip(),))) == 0:
                    break
            else:
                bad_attrs.append(bad_attr)
            continue
        if isinstance(attr, tuple) or "," in attr:
            if isinstance(attr, str):
                attr = attr.split(",")  # noqa: PLW2901
                if len(attr) != 2:
                    raise ValueError(f"Invalid attribute {attr}")
                attr, key = attr  # noqa: PLW2901
                attr = re.sub(check_attrs_filter, check_attrs_to_keep, attr)  # noqa: PLW2901
                key = re.sub(check_attrs_filter, check_attrs_to_keep, key)
            else:
                attr, key = attr  # noqa: PLW2901
            bad_attr = f"{attr}[{key}]"
            if hasattr(obj, attr):
                value = getattr(obj, attr)
                if value is None or key not in value or value[key] is None:
                    bad_attrs.append(bad_attr)
                continue
            bad_attrs.append(bad_attr)
            continue
        bad_attr = attr
        if hasattr(obj, attr):
            value = getattr(obj, attr)
        else:
            bad_attrs.append(bad_attr)
            continue
        if value is None:
            bad_attrs.append(bad_attr)
    return bad_attrs


def _check_kwargs(
    dictionary: dict,
    mandatory: list | tuple,
    allowed: list | tuple,
):
    """Checks if any keys are missing, or unexpected, in a given :obj:`dict`.

    Raises:
        ValueError: If some keyword arguments are missing or unexpected.
    """
    missing = [k for k in mandatory if k not in dictionary]
    forbidden = [k for k in dictionary if k not in allowed]
    error = ""
    if len(missing) > 0:
        error = "\n".join(["Missing kwargs:", "\n - ".join(missing)])
    if len(forbidden) > 0:
        error_forbidden = "\n".join(
            ["Unexpected kwargs:", "\n - ".join(forbidden)]
        )
        error = (
            "\n".join(
                [error, error_forbidden, "allowed:", "\n - ".join(allowed)]
            )
            if error
            else error_forbidden
        )
    if error:
        raise invalid_kwargs_err(error)
