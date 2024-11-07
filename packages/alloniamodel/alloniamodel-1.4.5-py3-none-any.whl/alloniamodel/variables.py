from typing import ClassVar

import numpy as np
import pandas as pd
from typeguard import typechecked

from .decorator import classproperty


class _VariablesIterator:
    def __init__(self, variables: "Variables"):
        self.attrs = []
        for item in Variables._ATTRIBUTES:
            if hasattr(variables, item):
                setattr(self, f"{item}", getattr(variables, item))
                self.attrs.append(item)
        self._size = len(variables)
        self._current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < self._size:
            variable = (
                getattr(self, f"{item}")[self._current_index]
                for item in self.attrs
            )
            self._current_index += 1
            return variable
        raise StopIteration


class Variables:
    """A collection of variable descriptions (not the ACTUAL data of the
    said variables).

    Used by :obj:`~aleiamodel.model.AleiaModel` to select predictive and
    target variables from various datasets. One element of an instance of
    :obj:`~Variables` must have a name and/or an index, unique in the object,
    that will be used to identify it. Names only work if datasets used in
    :obj:`~aleiamodel.model.AleiaModel` are
    :obj:`~pandas.DataFrame` objects. If both names and indexes are given,
    indexes are used.

    Examples:
        .. code-block:: python

            import numpy as np
            from sklearn.datasets import load_iris
                iris_dataset = load_iris()
                raw = np.concatenate(
                [iris_dataset["data"], iris_dataset["target"].reshape(-1, 1)],
                axis=1,
            )
            pred = Variables(
                indexes=tuple(range(4)),
                names=iris_dataset["feature_names"],
                descriptions=(..., ..., ..., ...),
                types=(float,) * len(iris_dataset["feature_names"]),
            )
    """

    _ATTRIBUTES: ClassVar = {
        "indexes": int,
        "names": str,
        "descriptions": str,
        "types": type,
        "classes": tuple,
    }

    @classproperty
    def handling_methods(cls):  # noqa: N805
        return {
            cls: lambda x: x,
            pd.DataFrame: cls.handle_dataframe,
            pd.Series: cls.handle_series,
            np.ndarray: cls.handle_array_or_index,
            pd.Index: cls.handle_array_or_index,
            dict: cls.handle_dict,
        }

    @classmethod
    def handle_input(cls, variables):
        if variables is None:
            return None

        type_v = type(variables)
        if type_v in cls.handling_methods:
            return cls.handling_methods[type_v](variables)

        if len(variables) == 0:
            return cls(indexes=[])
        if isinstance(variables[0], str):
            return cls(names=variables)
        return cls(indexes=variables)

    @classmethod
    def handle_dataframe(cls, variables):
        if variables.empty:
            return cls(indexes=[])
        if "names" in variables.index or "indexes" in variables.index:
            variables = variables.T
        # Let any error of missing attribute or wrong type be
        # raised by __init__
        return cls(
            **dict(
                pd.Series(
                    index=variables.columns,
                    data=variables.T.to_numpy().tolist(),
                )
            )
        )

    @classmethod
    def handle_series(cls, variables):
        return cls(indexes=[]) if variables.empty else cls(**dict(variables))

    @classmethod
    def handle_array_or_index(cls, variables):
        return (
            cls(indexes=list(variables))
            if variables.dtype in (np.int32, np.int64)
            else cls(names=list(variables))
        )

    @classmethod
    def handle_dict(cls, variables):
        return cls(**variables)

    def __init__(
        self,
        **kwargs,
    ):
        """
        Args:
            kwargs: Must contain at least one of "names" (strings) or
                "indexes" (integers) as keys. If both are present, "indexes"
                will be used to get the variables in the data. Else, will use
                either "indexes" or "names" depending on which is available.
                The other possible keys are "descriptions" and "types".
        """

        self.length = 0
        if "indexes" in kwargs:
            self.ref_name = "indexes"
        elif "names" in kwargs:
            self.ref_name = "names"
        else:
            raise ValueError("Please provide one of 'indexes' or 'names'")

        for item in self._ATTRIBUTES:
            values = kwargs.get(item, ())
            if len(values) == 0:
                continue
            length = len(values)
            if item == self.ref_name:
                self.length = length
                if len(set(values)) < length:
                    raise ValueError(
                        f"Can not have repeating {item} as they are used as "
                        f"unique identifiers here."
                    )
            elif length != self.length:
                raise ValueError(
                    f"Variables was provided with {length} {item}"
                    f" but {self.length} {self.ref_name}."
                )
            if item == "types":
                values = tuple(
                    value.type if hasattr(value, "type") else value
                    for value in values
                )
                kwargs["types"] = values
            if isinstance(values, pd.Index):
                values = values.tolist()
                kwargs[item] = values
            for value in values:
                expected = self._ATTRIBUTES[item]
                if not isinstance(value, expected):
                    raise TypeError(
                        f"A value in {item} is of type {type(value)} instead"
                        f" of type {expected}"
                    )
        self.data = {k: v for k, v in kwargs.items() if k in self._ATTRIBUTES}

    def __len__(self):
        return self.length

    def __getitem__(self, i: int):
        return tuple(
            self.data[item][i] for item in self._ATTRIBUTES if item in self.data
        )

    @property
    def identities(self):
        # Always return a list, as Variables.identities is used in dataframe
        # slicing, which does not work with tuples.
        return (
            list(self.data["names"])
            if self.ref_name == "names"
            else list(self.data["indexes"])
        )

    @property
    def indexes(self):
        return self.data.get("indexes", ())

    @property
    def names(self):
        return self.data.get("names", ())

    @property
    def descriptions(self):
        return self.data.get("descriptions", ())

    @property
    def types(self):
        """If types was never specified, it will be detected upon model
        training."""
        return self.data.get("types", ())

    @property
    def classes(self):
        """If classes was never specified, it will be detected upon model
        training."""
        return self.data.get("classes", ())

    def __add__(self, variables: "Variables"):
        if self.ref_name != variables.ref_name:
            raise ValueError(
                "Can not add variables that have different reference names. "
                "Both must be 'names' or both must be 'indexes'."
            )

        data = {}
        for item in self._ATTRIBUTES:
            attr_1 = getattr(self, item)
            attr_2 = getattr(variables, item)
            if bool(attr_1) != bool(attr_2):
                raise ValueError(
                    f"Can not add Variables object: one has '{item}' "
                    "but not the other"
                )
            if attr_1:
                data[item] = tuple(attr_1) + tuple(attr_2)
        return Variables(**data)

    @typechecked
    def __eq__(self, other: "Variables"):
        if self.length != other.length:
            return False
        return all(tuple(v1) == tuple(v2) for v1, v2 in zip(self, other))

    def __repr__(self):
        return f"'Variables' object : {self.data!s}"
