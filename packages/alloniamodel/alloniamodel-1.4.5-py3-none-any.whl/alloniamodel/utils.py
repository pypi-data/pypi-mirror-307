from __future__ import annotations

import inspect
import logging
import re
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Any, Callable, ClassVar

import numpy as np
import pandas as pd
from allonias3 import Configs, S3Path
from allonias3.helpers.responses import DeleteResponse, WriteResponse
from typeguard import typechecked

from .errors import (
    ReadOnlyError,
    VersionNotFoundError,
    data_type_err,
    fewer_revisions_than_data_err,
    invalid_revision_err,
    missing_loading_method_err,
)

if TYPE_CHECKING:
    from datetime import datetime

logger = logging.getLogger("alloniamodel.utils")

# Remove any leading/trailing whitespace, (, ), [ or ] and keep what is between
check_attrs_filter = r"^[\s\(\[]{0,}(?P<keep>.+?)[\s\]\)]{0,}$"
check_attrs_to_keep = r"\g<keep>"


def reshape(data, new_shape):
    if isinstance(data, (pd.DataFrame, pd.Series)):
        data = data.to_numpy()
    if new_shape is not None:
        data = data.reshape(new_shape)
    return data


def try_delete(path: S3Path, function: str, **kwargs) -> DeleteResponse:
    try:
        return getattr(path, function)(**kwargs)
    except Exception as error:
        return DeleteResponse(
            {
                "Errors": [
                    {
                        "Key": str(path),
                        "VersionId": kwargs.get("version_id"),
                        "Code": error.__class__.__name__,
                        "Message": str(error),
                    }
                ]
            }
        )


def get_type(np_type):
    """Converts numpy types to python types."""
    if np_type == np.object_:
        return object
    if np_type is str:
        return str
    np_element = np_type(0, "D") if "time" in np_type.__name__ else np_type(0)
    return type(np_element.item())


def get_variable(data, variables, which):
    """Will select the subset of variables we are interested in from data,
    squeeze it if only 1 variable is required, and detect their types if not
    already specified."""

    message = (
        f"AllOnIAModel could not detect the type of {which} "
        "variables. You can specify them by passing "
        "dictionaries like that to model.set_variables:\n"
        "{\n"
        f"   'names': {variables.identities},\n"
        "   'types': (...),\n"
        "}\n"
        "Where 'types' contains one python type per variable."
    )
    if isinstance(data, np.ndarray):
        subset = (
            data[:, variables.identities[0]]
            if len(variables) == 1
            else data[:, variables.identities]
        )
        if "types" not in variables.data:
            try:
                variables.data["types"] = tuple(
                    get_type(
                        type(subset[0] if len(variables) == 1 else subset[0, i])
                    )
                    for i in range(len(variables))
                )
            except Exception:
                variables.data["types"] = tuple(
                    "unknown" for _ in range(len(variables))
                )
                logger.warning(message)
        return subset
    subset = (
        data[variables.identities[0]]
        if len(variables) == 1
        else data[variables.identities]
    )
    try:
        if "types" not in variables.data:
            if isinstance(subset, (pd.DataFrame, pd.Series)):
                variables.data["types"] = tuple(
                    get_type(
                        type(
                            subset.iloc[0]
                            if len(variables) == 1
                            else subset.iloc[0, i]
                        )
                    )
                    for i in range(len(variables))
                )
            elif isinstance(subset, np.ndarray):
                variables.data["types"] = tuple(
                    get_type(
                        type(subset[0] if len(variables) == 1 else subset[0, i])
                    )
                    for i in range(len(variables))
                )
            else:
                variables.data["types"] = tuple(
                    "unknown" for _ in range(len(variables))
                )
                logger.warning(message)
    except Exception:
        variables.data["types"] = tuple(
            "unknown" for _ in range(len(variables))
        )
        logger.warning(message)
    return subset


def convert_columns(array, columns, factors):
    return array[columns].astype(float) / factors


def get_open_by() -> dict:
    """Returns the track, project and user ID running this function, and in
    which file.

    In case of a notebook, the file name will be meaningless (a random integer),
    so return information about the track, the project and the user instead.
    """

    track_id = str(Configs.instance.TRACK_ID)
    project_id = str(Configs.instance.PROJECT_ID)
    user_id = str(Configs.instance.user_id)

    open_by = {"track": track_id, "project": project_id, "user": user_id}

    try:
        # If running in a .py file, we can catch its path
        stack_trace = inspect.stack()
        filepath = stack_trace[2][1]
        open_by["file"] = filepath
    except ValueError:
        pass
    return open_by


def format_assets_history(assets_history: None | dict):
    if assets_history:
        return pd.DataFrame(
            {
                date: assets_history[date]["open_by"]
                for date, hist in assets_history.items()
                if isinstance(assets_history[date]["open_by"], dict)
            }
        ).T.drop_duplicates(keep="last")
    return pd.DataFrame()


def _get_versions_from_args(self, *args, **kwargs):
    rev_or_ver = args[0]
    versions = kwargs.get("versions", None)
    if versions is None:
        versions = self._get_model_versions()
        kwargs["versions"] = versions
    return rev_or_ver, versions, list(args[1:])


def format_version(func):
    """Assumes that the first argument passed to 'func' is either the revision
    number or the version ID. If the version ID is given, executes 'func'
    with it. If it is a revision number (possibly negative), executes 'func'
    with the corresponding version ID.

    Will raise in case of invalid revision number, or warn and return None if
    here are no versions for the associated model.
    """

    def _format_version(self, *args, **kwargs):
        rev_or_ver, versions, args = _get_versions_from_args(
            self, *args, **kwargs
        )

        if len(versions.index) == 0:
            logger.warning("Associated model has no versions.")
            return None

        if (
            isinstance(rev_or_ver, str)
            or rev_or_ver is None
            or rev_or_ver == -1
        ):
            # Is a version ID, or latest version
            if rev_or_ver == -1:
                rev_or_ver = None
            # Do not use the output as we want None to remain None. Just check
            # that the version is valid.
            check_valid_version(rev_or_ver, versions, self.model_kwargs["name"])
            return func(self, rev_or_ver, *args, **kwargs)
        revision, version, _ = check_valid_revision(
            rev_or_ver, versions, self.model_kwargs["name"]
        )
        return func(self, version, *args, **kwargs)

    return _format_version


def check_valid_revision(revision, versions, model_name):
    """Checks that a given revision is valid for a given model's versions df,
    and return the valid revision number and the associated version ID and its
    creation date.

    A negative revision will be converted to a positive revision number using
    revision -> revisions + revision + 1.

    Passing revision=0 or a revision number too big (positively or negatively)
    will produce a ValueError or VersionNotFoundError respectively.
    """
    revisions = len(versions.index)

    if revision is None:
        revision = -1
    if revision == 0:
        raise invalid_revision_err()
    if revision < 0:
        # Try to convert a negative revision to a positive revision. The next
        # check will ensure the positivity.
        revision = revisions + revision + 1
    if not 0 < revision <= revisions:
        # Revision is invalid for the given model
        raise VersionNotFoundError(model_name, revision=revision)
    # Revision number 1 is version[0], so use revision - 1
    version_line = versions.iloc[revision - 1]
    creation_date = version_line.name
    version = version_line["version"]
    return revision, version, creation_date


def check_valid_version(version, versions, model_name):
    """Checks that a given version ID exists for a given model's versions df,
    and return the associated revision number, the version ID and its creation
    date.

    One can pass None as version to get the information of the latest version.
    """
    if version is None:
        creation_date = versions.index[-1]
        version = versions["version"].to_numpy()[-1]
        revision = len(versions.index)
        return revision, version, creation_date
    if version not in versions["version"].to_numpy():
        raise VersionNotFoundError(model_name, version=version)
    creation_date = versions.loc[versions["version"] == version].index[0]
    revision = (
        versions.reset_index()[
            (versions["version"] == version).to_numpy()
        ].index[0]
        + 1
    )
    return revision, version, creation_date


class CustomPickleable(metaclass=ABCMeta):
    """
    See Also:
        https://docs.python.org/3.9/library/pickle.html
    """

    def __init__(self, *args, **kwargs):
        self.define(*args, **kwargs)

    @abstractmethod
    def define(self, *args, **kwargs):
        pass

    @abstractmethod
    def __getstate__(self): ...

    @abstractmethod
    def __setstate__(self, state): ...


class SpecialDataFormat:
    """If your data is not a :obj:`pandas.DataFrame`, :obj:`pandas.Series` nor a
    :obj:`numpy.ndarray`, you can store it in this object. It can be used in
    feature engineering and train-test split.

    Examples:
        .. code-block:: python

            from alloniamodel import AllOnIAModel, SpecialDataFormat
            from sklearn.feature_extraction.text import CountVectorizer
            from sklearn.model_selection import train_test_split

            data = [
                ("Offre spéciale ! Gagnez gros !", "spam"),
                ("Réunion demain à 14h.", "ham"),
                ("Vente exclusive en cours.", "spam"),
                ("Rappel : Facture à régler.", "ham")
            ]

            def feat_eng(emails):
                X = [email[0] for email in emails]
                y = [email[1] for email in emails]
                vectorizer = CountVectorizer()
                X_vectorized = vectorizer.fit_transform(X)
                return SpecialDataFormat(x=X_vectorized, y=np.array(y))

            def custom_train_test_split(data_, test_size, random_state):
                X_train, X_test, y_train, y_test = train_test_split(
                    data_.x,
                    data_.y,
                    test_size=test_size,
                    random_state=random_state
                )
                return (
                    SpecialDataFormat(x=X_train, y=y_train),
                    SpecialDataFormat(x=X_test, y=y_test)
                )

            model = AllOnIAModel(...)
            model.feature_engineering_function = feat_eng
            model.train_val_test_split_function = custom_train_test_split
            # 'x' and 'y' will match the 'x' and 'y' attribute of the
            # SpecialDataFormat. The line below is not mandatory, as those are
            # the default values for predictive and target variables.
            model.set_variables(("x",), ("y",))
    """

    def __init__(self, x, y):
        self.x = x
        """The predictive variables"""
        self.y = y
        """The target variables"""

    def __getitem__(self, item):
        """You can use :inlinepython:`["x"]` and :inlinepython:`["y"]` to access
        :obj:`~SpecialDataFormat.x` and :obj:`~SpecialDataFormat.y`.
        """
        if item == "x":
            return self.x
        if item == "y":
            return self.y
        raise ValueError(f"Invalid item {item}")

    @property
    def shape(self):
        return self.x.shape


class URL:
    """Use this class if your data comes from an external URL and needs to be
    downloaded before use.

    Note that this class does not support versioning.

    Attributes:
        url (str): The url to download from.
        s3_path (str): The s3 file to store the URL content in.
    """

    @typechecked
    def __init__(
        self,
        url: str,
        s3_path: S3Path,
    ):
        self.url = url
        self.s3_path = s3_path

    def __str__(self):
        return f"{self.url} {self.s3_path}"

    @typechecked
    def __call__(self, force: bool) -> None | WriteResponse:
        if force or not self.s3_path.is_file():
            return self.s3_path.write(self.url)
        return None


class DataHandler(CustomPickleable):
    """A class that can handle data in the form of :obj:`str` (a path to S3),
    :obj:`~numpy.ndarray`, :obj:`~pandas.DataFrame`,
    :obj:`~pandas.Series`:obj:`str`, a collections of :obj:`str` (paths to s3),
    :obj:`SpecialDataFormat` or obj:`URL`.

    Can also be created empty.

    The created instance is a callable which, when called, returns the data
    associated to it as None (if empty), the :obj:`~numpy.ndarray`,
    :obj:`~pandas.DataFrame`, :obj:`~pandas.Series` or :obj:`SpecialDataFormat`
    that was given to it, the content of the file pointed by the given path, or
    the aggregated content of the files pointed by the given path.

    Attributes:
        _type_to_suffix (dict): Intermediate data will be saved in files whose
            suffix depends on the data type.
        attached_to (AllOnIAModel): The model this object is attached to.
        pointer (None | str | tuple | URL): The path where the data is located.
            If a string or a collection of strings was given, they are kept
            here. If the persistency of the data is activated in the attached
            model, the path where the data is written
            is saved here too. If an :obj:`URL` was given, it is kept here.
        _data (Any): The actual data, or :inlinepython:`None` if not yet called.
        _method (str): How to get the data (from a file, from an url, from
            multiple files...)
        _revision (int | None): The revision number of the data. Set when the
            object is called and the data loaded.
        concatenate_kwargs (dict): If a collection of strings was given, an
            aggregation is done on the data read from all the files.
            Arguments valid for :obj:`pandas.concat` or :obj:`numpy.concatenate`
            can be given here.
        force_download (bool): If a :obj:`URL` was given, you can force it to
            re-download the data even if it has already been.
        _revision_to_use (None | int | tuple): The revision(s) to use when
            loading the file(s).
        handle_type (bool): Set this attribute to :inlinepython:`False`
            to just unpickle any file instead of trying to
            return a specific object type based on the file extension.
        load_kwargs (dict): kwargs to pass to :obj:`~aleialib.s3.s3.load_file`.
            You can give :inlinepython:`{"index_col": None}` for example, if
            your **.csv** files do not have index.

    """

    _type_to_suffix: ClassVar = {
        dict: ".json",
        pd.DataFrame: ".parquet",
        pd.Series: ".parquet",
        np.ndarray: ".npy",
        URL: ".pkl",
        SpecialDataFormat: ".pkl",
    }

    default_kwargs: ClassVar = {
        "revision": None,
        "concatenate_kwargs": {},
        "force_download": False,
        "revision_to_use": None,
        "handle_type": True,
        "load_kwargs": {"index_col": 0},
        "persist_to": None,
    }

    @typechecked
    def __init__(
        self,
        attached_to,
        data: S3Path
        | tuple[S3Path, ...]
        | list[S3Path]
        | np.ndarray
        | pd.DataFrame
        | pd.Series
        | SpecialDataFormat
        | URL
        | None = None,
        persist_to: str | None = None,
    ):
        """
        Args:
            attached_to (AllOnIAModel): The instance of
                :obj:`~alloniamodel.model.AllOnIAModel` this object is attached
                to.
            data: the data to handle.
            persist_to: if specified and if data is a
                :obj:`~numpy.ndarray`, a :obj:`~pandas.DataFrame`, or
                a :obj:`~pandas.Series`, will save the data in
                :obj:`~alloniamodel.model.AllOnIAModel.intermediary_save_path`
                :inlinepython:`/{persist_to}.parquet` or
                :obj:`~alloniamodel.model.AllOnIAModel.intermediary_save_path`
                :inlinepython:`/{persist_to}.parquet`. If it is a
                :obj:`SpecialDataFormat`, it will be pickled in
                :obj:`~alloniamodel.model.AllOnIAModel.intermediary_save_path`
                :inlinepython:`/{persist_to}.pkl`
        """
        self.attached_to = None
        self.pointer: S3Path | list[S3Path] | URL | None = None
        self._data = None
        self._method = None
        self._revision = None
        self.concatenate_kwargs = None
        self.force_download = None
        self._revision_to_use = None
        self.handle_type = None
        self.load_kwargs = None
        super().__init__(
            attached_to=attached_to,
            data=data,
            persist_to=persist_to,
        )

    @typechecked
    def use_revision(
        self,
        revision: int | tuple[int | None, ...] | list[int | None] | None,
    ):
        """Only valid if the object was given a path or a collection of paths.

        Will load the specified revision(s) instead of the latest one(s).

        In the case of a collection of files, either give one revision (same for
        all files), or a list or tuple of revisions. In that case, there must be
        one value per file.

        To use the latest version, either use None or -1 for a revision.
        """
        if (isinstance(revision, int) and revision == 0) or (
            not isinstance(revision, int) and 0 in revision
        ):
            raise invalid_revision_err()
        if self._method in ("", "from_file", "from_files"):
            self._revision_to_use = revision
            if self._method in ("from_file", "from_files"):
                # Force the DataHandler object to re-read the data next time it
                # is called.
                self._data = None

    @property
    def pointer_str(self) -> None | str | list[str]:
        if not self.pointer:
            return None
        if isinstance(self.pointer, (S3Path, URL)):
            return str(self.pointer)
        return [str(p) for p in self.pointer]

    def define(  # noqa: PLR0912
        self,
        attached_to,
        data,
        revision: int | None = None,
        concatenate_kwargs: dict | None = None,
        force_download: bool = False,
        revision_to_use: int | None = None,
        handle_type: bool = True,
        load_kwargs: dict | None = None,
        persist_to: str | None = None,
    ):
        if concatenate_kwargs is None:
            concatenate_kwargs = {}
        if load_kwargs is None:
            load_kwargs = {"index_col": 0}
        self.attached_to = attached_to
        self._revision = None
        self._revision_to_use = None
        self.concatenate_kwargs = concatenate_kwargs
        self.force_download = force_download
        self.handle_type = handle_type
        self.load_kwargs = load_kwargs

        if data is None:
            self.pointer = None
            self._data = None
            self._method = "empty"
        elif isinstance(data, S3Path):
            self.pointer = data
            self.handle_type = data.handle_type
            self._data = None
            self._method = "from_file"
            self._revision = revision
            self._revision_to_use = revision_to_use
        elif isinstance(data, (list, tuple)):
            self.pointer = []
            for p in data:
                if isinstance(p, S3Path):
                    self.pointer.append(p)
                    self.handle_type = p.handle_type
                else:
                    raise data_type_err(type(p))
            self._data = None
            self._method = "from_files"
            self._revision = revision
            self._revision_to_use = revision_to_use
        elif isinstance(data, URL):
            self.pointer = data
            if persist_to is not None:
                self.pointer.s3_path = data.s3_path
            self._data = None
            self._method = "from_url"
        elif isinstance(
            data, (np.ndarray, pd.DataFrame, pd.Series, SpecialDataFormat)
        ):
            self.pointer = None
            self._data = data
            self._method = ""
            if persist_to is not None:
                self.pointer = self._persist_intermediate_data(data, persist_to)
        else:
            # Should never arrive here thanks to typechecked
            raise data_type_err(type(data))

    def __call__(self):  # noqa: PLR0912, C901
        if self._data is None and self._method != "empty":
            if self._method == "from_file":
                self._revision = self._revision_to_use
                if self.pointer.suffix != ".csv":
                    self.load_kwargs.pop("index_col", None)
                self._data = self.pointer.read(
                    revision=self._revision_to_use, **self.load_kwargs
                )
                if self._revision is None:
                    self._revision = len(self.pointer.versions())
            elif self._method == "from_files":
                if self._revision_to_use is None:
                    self._revision_to_use = [None] * len(self.pointer)
                if not isinstance(self._revision_to_use, (tuple, list)) or len(
                    self._revision_to_use
                ) != len(self.pointer):
                    raise fewer_revisions_than_data_err(
                        self._revision_to_use, len(self.pointer)
                    )
                self._revision = self._revision_to_use

                arguments = []
                for pointer, revision in zip(
                    self.pointer, self._revision_to_use
                ):
                    arguments.append(
                        (
                            pointer,
                            {
                                "revision": revision,
                                **self.load_kwargs,
                            },
                        )
                    )
                    if pointer.suffix != ".csv":
                        arguments[-1][1].pop("index_col", None)
                with ThreadPoolExecutor() as executor:
                    data = list(
                        executor.map(
                            lambda x: S3Path.read(x[0], **x[1]), arguments
                        )
                    )
                    self._revision = [
                        len(obj)
                        if self._revision[i] is None
                        else self._revision[i]
                        for i, obj in enumerate(
                            executor.map(
                                lambda x: S3Path.versions(x),
                                self.pointer,
                            )
                        )
                    ]
                if isinstance(data[0], np.ndarray):
                    self._data = np.concatenate(data, **self.concatenate_kwargs)
                elif isinstance(data[0], (pd.DataFrame, pd.Series)):
                    self._data = pd.concat(data, **self.concatenate_kwargs)
                    try:
                        self._data.columns = self._data.columns.astype(int)
                    except (ValueError, TypeError) as e:
                        if "invalid literal for int()" in str(
                            e
                        ) or "Cannot cast Index to dtype " in str(e):
                            pass
                        else:
                            raise e
            elif self._method == "from_url":
                self.pointer(force=self.force_download)
                if self.pointer.s3_path.suffix != ".csv":
                    self.load_kwargs.pop("index_col", None)
                self._data = self.pointer.s3_path.read(**self.load_kwargs)
            else:
                raise missing_loading_method_err(self._method)
        return self._data

    def __getstate__(self):
        return (
            self.attached_to,
            self.pointer if self.pointer else None,
            self._revision,
            self.concatenate_kwargs,
            self.force_download,
            self._revision_to_use,
            self.handle_type,
            self.load_kwargs,
        )

    def __setstate__(self, state):
        self.define(*state, persist_to=None)

    def _persist_intermediate_data(
        self, data, name_without_suffix: str
    ) -> None | S3Path:
        """Saves the dataset :inlinepython:`name_without_suffix` to
        :obj:`~alloniamodel.model.AllOnIAModel.intermediary_save_path`
        :inlinepython:`/{persist_to}.xxx` (csv, parquet, npy or pickle)
        if :obj:`~alloniamodel.model.AllOnIAModel.save_intermediary_data` is
        True, or, if it is a :obj:`list` or :obj:`tuple`, if
        :inlinepython:`name_without_suffix` is in it.

        :inlinepython:`name_without_suffix` can end by :inlinepython:`_set` or
        not, it does not matter.

        Raises:
            ReadOnlyError: if the attached model is read-only.

        Returns:
            :
                :inlinepython:`None` if nothing was saved, or the path on S3 the
                data was saved to.
        """
        if (
            isinstance(self.attached_to.save_intermediary_data, bool)
            and self.attached_to.save_intermediary_data is False
        ) or (
            isinstance(self.attached_to.save_intermediary_data, (list, tuple))
            and name_without_suffix.rstrip("_set")
            not in self.attached_to.save_intermediary_data
            and name_without_suffix
            not in self.attached_to.save_intermediary_data
        ):
            return None
        if self.attached_to.read_only:
            raise ReadOnlyError("Can not save : model is read-only")

        suffix = self._type_to_suffix.get(data.__class__, ".pkl")
        path_with_suffix = S3Path(
            self.attached_to.intermediary_save_path / name_without_suffix,
            handle_type=self.handle_type,
        ).with_suffix(suffix)

        _ = path_with_suffix.write(data)
        return path_with_suffix


class Description:
    """A class that handles the model's description.

    It is a :obj:`dict`, in which some keys can be modified by the user
    through :obj:`~alloniamodel.model.AllOnIAModel.update_description`,
    and some are automatically defined when setting corresponding
    attributes in the model.

    Attributes:
        VALID_USER_ENTRIES (dict): User-specified entries. The keys match the
            keys in the underlying :obj:`dict`, the values are the default if
            the user did not specify anything.
        VALID_AUTO_ENTRIES (dict): Automatically filled when the model is
            updated. The keys match an attribute in a
            :obj:`~alloniamodel.model.AllOnIAModel` instance, the values are
            either entries or :obj:`tuple` of entries which are to be updated
            when the attribute changes.
        EXTERNAL_ENTRIES (dict): Filled by external sources (unused as of now,
            future feature).
        dict (dict): the underlying object containing the description.

    """

    data_template: ClassVar = {
        "Data description": "MISSING -- Details about data used by the "
        "model, through exploration to training. Also give details about"
        " annotation methodology that was potentially used to "
        "create the training dataset.",
        "Data location": {
            "Raw (learning set)": "",
            "Derived": "",
            "Train": "",
            "Validation": "",
            "Test": "",
            "Observations (set on which to make prediction)": "",
            "Derived observations": "",
            "Predictions": {
                "train": "",
                "validation": "",
                "test": "",
                "observations": "",
            },
            "Postprocessed predictions": "",
        },
        "Data summary": {
            "Predictive variable(s)": {},
            "Target variable(s)": {},
        },
    }

    VALID_USER_ENTRIES: ClassVar = {
        "Summary": "MISSING -- Details about functional context, model"
        " objectives, and various stakeholders.",
        "Status": "MISSING -- Details about model lifecycle status. Is it "
        "still in experiment or is it live ?",
        "Data": data_template,
        "Ethic": "MISSING -- Details about ethic studies done around model"
        " data, if existing biases were addressed or not (through"
        " synthetic data for example), and the process used "
        "(through ethic comity for example).",
        "Training": "MISSING -- Details about training frequency, data "
        "scope, and targeted lifecycle (hot or cold).",
        "Explainability": "MISSING -- Details about model explicability and"
        " potential libraries that are used to addressed"
        " this topic.",
        "Tests": "MISSING -- Details about test scenarios around the model,"
        " parameters control, data preparation, and expected "
        "values.",
        "Functional validation": "MISSING -- Details about the model"
        " functionnal validation and its"
        " methodology. Did it involve functional"
        " stakeholders doing annotation & "
        "validation campaigns and how was it"
        " done ?",
        "Activations": "MISSING -- Details about rules to control the model"
        " activation & deactivation on live environment.",
        "Deployment checklist": "MISSING -- list of requirements to check "
        "before being officially able to trigger a"
        " new model deployment.",
    }

    VALID_AUTO_ENTRIES: ClassVar = {
        "model": "Architecture",
        "model_class": "Architecture",
        "_requirements": "Architecture",
        "_seldon_implementation": "Architecture",
        "split_execs": "Technical performances",
        "feature_engineering_execs": "Technical performances",
        "learn_execs": ("Evaluation", "Technical performances"),
        "train_execs": "Technical performances",
        "validate_execs": ("Evaluation", "Technical performances"),
        "test_execs": ("Evaluation", "Technical performances"),
        "apply_execs": "Technical performances",
        "predict_execs": "Technical performances",
        "postprocess_execs": "Technical performances",
        "_raw_set": "Data location",
        "_derived_set": "Data location",
        "_train_set": "Data location",
        "_validation_set": "Data location",
        "_test_set": "Data location",
        "_observations_set": "Data location",
        "_derived_observations_set": "Data location",
        "_predictions": "Data location",
        "_postprocessed_predictions_set": "Data location",
        "_predictive_variables": "Data summary",
        "_target_variables": "Data summary",
        "_validators": "Rapporteurs",
        "_input_sample": "Data summary",
        "_output_sample": "Data summary",
    }

    DATA_LOCATION_CORRESPONDANCE: ClassVar = {
        "_raw_set": "Raw (learning set)",
        "_derived_set": "Derived",
        "_train_set": "Train",
        "_validation_set": "Validation",
        "_test_set": "Test",
        "_observations_set": "Observations (set on which to make prediction)",
        "_derived_observations_set": "Derived observations",
        "_postprocessed_predictions_set": "Postprocessed predictions",
    }

    VALID_AUTO_ENTRIES_VALUES: ClassVar = {
        "Architecture": "_update_architecture",
        "Technical performances": "_update_tech_perf",
        "Evaluation": "_update_evaluation",
        "Data summary": "_update_data_summary",
        "Data location": "_update_data_location",
        "Rapporteurs": "_update_rapporteurs",
    }

    EXTERNAL_ENTRIES: ClassVar = {
        "Feedback loop": "Details about the validation & improvement"
        " process based on the live model inferences."
    }

    def __init__(self, obj, entries):
        self._dict = {}
        if obj:
            self.dict: dict[str, Any] = self.VALID_USER_ENTRIES.copy()
            self.update_user_entries(entries)
            for key in self.VALID_AUTO_ENTRIES:
                self.update_auto_entry(key, obj)
        else:
            self.dict: dict[str, Any] = entries

    @property
    def dict(self) -> dict:
        return self._dict

    @dict.setter
    def dict(self, value: dict):
        self._dict = value
        if "Technical performances" in value:
            if "Learnings" in value["Technical performances"]:
                self._dict["Technical performances"][
                    "Learnings"
                ].index.name = "date"
            if "Predicts" in value["Technical performances"]:
                self._dict["Technical performances"][
                    "Predicts"
                ].index.name = "date"

    def update_user_entries(self, entries: dict):
        """Updates this object's :obj:`dict` with user-defined values."""
        for entry in entries.copy():
            if entry not in self.VALID_USER_ENTRIES:
                if entry not in self.VALID_AUTO_ENTRIES_VALUES:
                    valid_entries = "\n * ".join(self.VALID_USER_ENTRIES)
                    logger.warning(
                        f"Description entry '{entry}' is unexpected and"
                        " will be ignored. Valid entries are \n * "
                        f"{valid_entries}"
                    )
                del entries[entry]
            else:
                if not isinstance(entries[entry], str):
                    raise ValueError(
                        f"Can only provide strings to description entries, not"
                        f" {type(entries[entry])}"
                    )
                if entry == "Data":
                    if isinstance(self._dict[entry], str):
                        self._dict[entry] = self._data_template
                    entries[entry] = {
                        "Data description": entries[entry],
                        "Data location": self._dict[entry]["Data location"],
                        "Data summary": self._dict[entry]["Data summary"],
                    }
        if len(entries) > 0:
            self._dict.update(entries)
            return True
        return False

    def update_auto_entry(self, entry, obj):
        """Updates this object's :obj:`dict` with a value extracted from
        a :obj:`~alloniamodel.model.AllOnIAModel` instance.
        The updated entry depends on the name of the attribute the value was
        extracted from."""
        to_updates = self.VALID_AUTO_ENTRIES[entry]
        if isinstance(to_updates, str):
            to_updates = (to_updates,)
        for to_update in to_updates:
            getattr(self, self.VALID_AUTO_ENTRIES_VALUES[to_update])(obj, entry)

    def _update_architecture(self, obj, entry):
        to_update = "Architecture"
        if to_update not in self._dict:
            self._dict[to_update] = {}
        value = getattr(obj, entry)
        if entry == "model":
            self._dict[to_update]["Model"] = (
                None if value is None else value.__class__.__name__
            )
        elif entry == "model_class":
            self._dict[to_update]["Model"] = (
                None if value is None else value.__name__
            )
        elif entry == "_requirements":
            self._dict[to_update]["Requirements"] = (
                None if value is None else obj.get_requirements().split("\n")
            )
        elif entry == "_seldon_implementation":
            self._dict[to_update]["Seldon Implementation"] = (
                None if value is None else value
            )

    def _update_tech_perf(self, obj, _):
        dataframes = [
            obj.feature_engineering_execs.summary[["duration"]],
            obj.split_execs.summary[["duration"]],
            obj.train_execs.summary[["duration"]],
            obj.validate_execs.summary[["duration"]],
            obj.test_execs.summary[["duration"]],
            obj.predict_execs.summary[["duration"]],
            obj.postprocess_execs.summary[["duration"]],
        ]
        dataframes = pd.concat(
            [
                dataframe.mean().round(2).astype(str)
                + "+/-"
                + dataframe.std().round(2).astype(str)
                for dataframe in dataframes
            ],
            axis=1,
        )
        dataframes.columns = [
            "Feature engineering",
            "Train-validation-test split",
            "Training",
            "Validation",
            "Test",
            "Prediction",
            "Postprocess",
        ]
        dataframes.index = ["Duration (s)"]
        to_update = "Technical performances"
        if to_update not in self._dict:
            self._dict[to_update] = {}
        self._dict[to_update]["Durations"] = dataframes.T
        self._dict[to_update]["Learnings"] = obj.learnings_summary
        self._dict[to_update]["Predicts"] = obj.applies_summary

    def _update_evaluation(self, obj, _):
        to_update = "Evaluation"
        if to_update not in self._dict:
            self._dict[to_update] = {
                "Validation metrics": {},
                "Test metrics": {},
            }
        validations = obj.validate_execs.content
        tests = obj.test_execs.content
        if len(validations) > 0:
            self._dict[to_update]["Validation metrics"] = validations[
                -1
            ].results
        if len(tests) > 0:
            self._dict[to_update]["Test metrics"] = tests[-1].results

    def _update_data_location(self, obj, entry):
        parent = "Data"
        self._reset_data_if_need_be()
        value = getattr(obj, entry)
        if entry in self.DATA_LOCATION_CORRESPONDANCE:
            if value.pointer:
                location = (
                    str(value.pointer)
                    if isinstance(value.pointer, S3Path)
                    else [str(p) for p in value.pointer]
                )
            else:
                location = None

            self._dict[parent]["Data location"][
                self.DATA_LOCATION_CORRESPONDANCE[entry]
            ] = location
        elif entry == "_predictions":
            if "Predictions" not in self._dict[parent]["Data location"]:
                self._dict[parent]["Data location"]["Predictions"] = {}
            for dataset in value:
                if value[dataset].pointer:
                    location = (
                        str(value[dataset].pointer)
                        if isinstance(value[dataset].pointer, S3Path)
                        else [str(p) for p in value[dataset].pointer]
                    )
                else:
                    location = None
                self._dict[parent]["Data location"]["Predictions"][dataset] = (
                    location
                )
        # Else, should not happen but just do nothing

    def _update_data_summary(self, obj, entry):  # noqa: C901
        def format_variables(variables) -> dict:
            to_return = {}
            if variables is None:
                return to_return
            for i in range(len(variables)):
                to_return[variables.data[variables.ref_name][i]] = {}
                for attribute in variables._ATTRIBUTES:
                    if (
                        attribute in variables.data
                        and attribute != variables.ref_name
                    ):
                        single_attribute = attribute.rstrip("s")
                        value_ = variables.data[attribute][i]
                        if single_attribute == "indexe":
                            single_attribute = "index"
                        elif single_attribute == "type":
                            value_ = str(value_)
                        elif single_attribute == "classe":
                            single_attribute = "classes"
                        to_return[variables.data[variables.ref_name][i]][
                            single_attribute
                        ] = value_
            return to_return

        parent = "Data"
        self._reset_data_if_need_be()
        if entry not in ("_input_sample", "_output_sample"):
            value = format_variables(getattr(obj, entry))
        else:
            value = getattr(obj, entry)

        if "Predictive variable(s)" not in self._dict[parent]["Data summary"]:
            self._dict[parent]["Data summary"]["Predictive variable(s)"] = {}
        if "Target variable(s)" not in self._dict[parent]["Data summary"]:
            self._dict[parent]["Data summary"]["Target variable(s)"] = {}

        if entry == "_predictive_variables":
            example = self._dict[parent]["Data summary"][
                "Predictive variable(s)"
            ].get("Input Example")
            self._dict[parent]["Data summary"]["Predictive variable(s)"] = value
            if example:
                self._dict[parent]["Data summary"]["Predictive variable(s)"][
                    "Input Example"
                ] = example
        elif entry == "_target_variables":
            example = self._dict[parent]["Data summary"][
                "Target variable(s)"
            ].get("Output Example")
            self._dict[parent]["Data summary"]["Target variable(s)"] = value
            if example:
                self._dict[parent]["Data summary"]["Target variable(s)"][
                    "Output Example"
                ] = example
        elif entry == "_input_sample":
            self._dict[parent]["Data summary"]["Predictive variable(s)"][
                "Input Example"
            ] = value if value else "No example to display"
        elif entry == "_output_sample":
            self._dict[parent]["Data summary"]["Target variable(s)"][
                "Output Example"
            ] = value if value else "No example to display"

    def _update_rapporteurs(self, obj, _):
        entry = "Rapporteurs"
        self._dict[entry] = [dict(validator) for validator in obj._validators]

    def _reset_data_if_need_be(self):
        if "Data" not in self._dict:
            self._dict["Data"] = self.data_template
        if isinstance(self._dict["Data"], str):
            previous_data = self._dict["Data"]
            self._dict["Data"] = self.data_template
            self._dict["Data"]["Data description"] = previous_data


@dataclass
class _Validator:
    """Represents a real person in charge of monitoring a model.

    Attributes:
        name (str): The name or name and surname of the person.
        email (str): The email of the person.
        role (str): The role of the person.

    """

    name: str
    email: str
    role: str
    regex_email = r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$"

    def __post_init__(self):
        if not re.match(self.regex_email, self.email):
            raise ValueError(
                f"Validator {self.name}'s email '{self.email} is not valid."
            )

    def __str__(self):
        return f"{self.name} ({self.email}) : {self.role}"

    def __iter__(self):
        yield "name", self.name
        yield "email", self.email
        yield "role", self.role


@dataclass
class _Requirement:
    """A class representing an installed python package, or Python itself.

    An instance of this class is equal to another if they have the same name,
    no matter their versions. As a string, it will be
    ":obj:`name` == :obj:`version`"
    so that it can be used to create a *requirements.txt* file easily.

    Attributes:
        name (str): The name of the package (numpy, pandas...).
        version (str): The version of the package (0.15.`, ...).
    """

    name: str
    version: str

    def __eq__(self, other):
        return (
            self.name == other
            if isinstance(other, str)
            else self.name == other.name
        )

    def __str__(self):
        return f"{self.name}=={self.version}"


class BackwardCompatibleObject:
    """This class allows a class that is supposed to be pickled and loaded
    to support changes in its attributes. For example, suppose your class
    :inlinepython:`A` has no attribute :inlinepython:`a` in its first version.
    You pickle an instance of it, but then you load it with a new version of
    :inlinepython:`A`, where :inlinepython:`a` is a valid attribute.
    If you then call :inlinepython:`A.a`, it will result in a
    :obj:`AttributeError`.

    But if your class :inlinepython:`A` derives from this metaclass, you must
    define :obj:`~BackwardCompatibleObject.deleted_attributes`,
    :obj:`~BackwardCompatibleObject.renamed_attributes` and
    :obj:`~BackwardCompatibleObject.new_attributes` that will handle any new,
    old or renamed attributes, by returning custom default values and print
    custom warning messages.
    """

    class DeletedAttributeError(Exception):
        pass

    class NewAttributeError(Exception):
        pass

    class RenamedAttributeError(Exception):
        pass

    @property
    def deleted_attributes(self) -> dict:
        """If your new version does not support a given attribute, you can
        add it to this :obj:`dict` like that :

        .. code-block:: python

            from aleialib.helpers import BackwardCompatibleObject

            class A(BackwardCompatibleObject):
                deleted_attributes = {
                    "a": {
                        "warning": "Calling an attribute from an older version
                                   "of A. Attribue 'a' should not be used
                                   "anymore."
                        "default": None
                    }
                }
                ...

        Then, calling the attribute :inlinepython:`a` can result in two things:

          1. If you are calling an old version, that sill defines
             :inlinepython:`a`, the warnings message will be printed, but the
             existing value of :inlinepython:`a` will still be returned.
          2. If you are calling a new version, where :inlinepython:`a` is not
             defined, the warnings message will be printed and
             :inlinepython:`None` will be returned.
          3. If instead of "warning" you used the keyword "error",
             :obj:`~DeletedAttributeError` is raised.

        Note that this warning and :inlinepython:`None` are the default values,
        so you could just have done :

        .. code-block:: python

            from aleialib.helpers import BackwardCompatibleObject

            class A(BackwardCompatibleObject):
                deleted_attributes = {"a": {}}
                ...

        You can also specifiy a function that takes the class instance as
        argument as the default value
        (see :obj:`~BackwardCompatibleObject.new_attributes`).
        """
        return {}

    @property
    def renamed_attributes(self) -> dict:
        """If you renamed an attribute in your new version, you can add it to
        this :obj:`dict` like that :

        .. code-block:: python

            from aleialib.helpers import BackwardCompatibleObject

            class A(BackwardCompatibleObject):
                renamed_attributes = {
                    "a": {
                        "warning": "Using an old version of A. "
                                   "Attribue 'b' is now called 'a'.",
                        "old_name": "b",
                        "set": True,
                    }
                }
                ...

        Then, calling :inlinepython:`A.a` will warn and return
        :inlinepython:`None` instead of raising if using an older version
        that does not define it. Also, :inlinepython:`A.a` is now set to
        :inlinepython:`None` (if "set" is True, which is the default).

        Calling :inlinepython:`A.b` will just raise an :obj:`AttributeError`,
        unless you specified it in
        :obj:`~BackwardCompatibleObject.deleted_attribute`.

        Note that this warning and :inlinepython:`None` are the default values,
        so you could just have done :

        .. code-block:: python

            from aleialib.helpers import BackwardCompatibleObject

            class A(BackwardCompatibleObject):
                new_attributes = {"a": {}}
                ...
        """
        return {}

    @property
    def new_attributes(self) -> dict:
        """If your new version supports a new attribute that was not in a
        previous version, you can add it to this :obj:`dict` like that :

        .. code-block:: python

            from aleialib.helpers import BackwardCompatibleObject

            class A(BackwardCompatibleObject):
                new_attributes = {
                    "a": {
                        "warning": "Using an old version of A that does not"
                                   " define 'a'. It will be None.",
                        "default": None,
                        "set": True,  # Default. True to not save the attribute.
                    }
                }
                ...

        Then, calling :inlinepython:`A.a` will warn and return
        :inlinepython:`None` instead of raising if using an older version
        that does not define it. Also, :inlinepython:`A.a` is now set to
        :inlinepython:`None` if "set" is True (default).

        It is recommended to do use "set=False" when managing new properties.

        Note that this warning and :inlinepython:`None` are the default values,
        so you could just have done :

        .. code-block:: python

            from aleialib.helpers import BackwardCompatibleObject

            class A(BackwardCompatibleObject):
                new_attributes = {"a": {}}
                ...

        You can also specifiy a function that takes the class instance as
        argument as the default value:

        .. code-block:: python

            from aleialib.helpers import BackwardCompatibleObject

            def _get_length_for_older_version(obj):
                return len(obj.iterabe)

            class A(BackwardCompatibleObject):
                new_attributes = {
                    "length": {
                        "default": _get_length_for_older_version
                    }
                }

                def __init__(self, iterable):
                    self.iterable = iterable
                    # length added in version x.x.x
                    self.length = len(iterable)

        """
        return {}

    def _default_deleted_warning(self, name):
        return (
            f"Using an old version of {self.__class__.__name__}."
            f" Attribue '{name}' should not be used anymore."
        )

    def _default_renamed_warning(self, name, old_name):
        return (
            f"Using an old version of {self.__class__.__name__}."
            f" Attribue '{old_name}' is now called '{name}'."
        )

    def _default_new_warning(self, name, default):
        return (
            f"Using an old version of {self.__class__.__name__} that does not."
            f" define '{name}'. It will be {default}."
        )

    @staticmethod
    def _handle_error(look_in, error):
        error_message = look_in.get("error", None)
        if error_message:
            raise error(error_message)

    def __getattribute__(self, item):
        # __getattribute__ is called when any attribute is looked for in the
        # object.
        deleted = super().__getattribute__("deleted_attributes")
        if item in deleted:
            self._handle_error(deleted[item], self.DeletedAttributeError)
            warning = deleted[item].get(
                "warning", self._default_deleted_warning(item)
            )
            if warning is not None:
                logger.warning(warning)
            try:
                return super().__getattribute__(item)
            except AttributeError:
                default = deleted[item].get("default", None)
                if isinstance(default, Callable):
                    default = default(self)
                return default
        return super().__getattribute__(item)

    def __getattr__(self, item):
        # __getattr__ is called when __getattribute__ did not find the
        # attribute in the object.
        renamed = super().__getattribute__("renamed_attributes")
        new = super().__getattribute__("new_attributes")
        if item in renamed:
            self._handle_error(renamed[item], self.RenamedAttributeError)
            old_name = renamed[item].get("old_name")
            warning = renamed[item].get(
                "warning", self._default_renamed_warning(item, old_name)
            )
            # will trigger __getattribute__ on the old name, which should exist.
            value = getattr(self, old_name)
            if warning is not None:
                logger.warning(warning)
            if renamed[item].get("set", True):
                setattr(self, item, value)
            return value
        if item in new:
            self._handle_error(new[item], self.NewAttributeError)
            warning = new[item].get("warning", None)
            default = new[item].get("default", None)
            if isinstance(default, Callable):
                default = default(self)
            if warning is not None:
                logger.warning(warning)
            if new[item].get("set", True):
                setattr(self, item, default)
            return default
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )


@dataclass
class ExecutionMetadata(BackwardCompatibleObject):
    """Can be used to store metadata about a run of a class method. Intended
    to be used on :obj:`~alloniamodel.model.AllOnIAModel` only.

    Attributes:
        date (datetime): When the function ran.
        dataset_revision (dict): the dataset(s) path(s) and its(their)
            revision(s). Both can be :inlinepython:`None` if the dataset was not
            given as a path or a collection of paths.
        model (str): name of the AI model class (LinearRegression, XGBoost, ...)
        duration (float): How long the execution lasted (in seconds).
        parameters (dict): keyword arguments passed to the function.
        results (Any): What the function returned. This is not always recorded,
            as it can be heavy.
        version_id (str): The version_id number of the model instance
            that created this object.

    See Also:
        :obj:`~alloniamodel.decorator._record_execution`
    """

    date: datetime
    dataset_revision: dict
    model: str
    duration: float = field(metadata={"unit": "s"})
    parameters: dict = field(default_factory=dict)

    version_id: str = None
    results: Any = None


class ExecutionList:
    """A collection of :obj:`~ExecutionMetadata`

    Attributes:
        content (list): All the :obj:`~ExecutionMetadata` recorded in this
            instance.
        model (AllOnIAModel): the model this object belongs to
    """

    def __init__(self, model):
        self.content: list[ExecutionMetadata] = []
        self.model = model

    @property
    def summary(self):
        """Produces a :obj:`~pandas.DataFrame` of each :obj:`~ExecutionMetadata`
        in this object, indexed by the run date."""
        existing_versions = self.model.list_versions(self.model.name)
        # important to cast the generators as list, otherwise we end up with
        # the same line repeating itself, I do not know why.
        df_execs = pd.DataFrame(
            data=[
                [getattr(e, attr.name) for attr in fields(ExecutionMetadata)]
                for e in self.content
            ]
            if self.content
            else None,
            columns=[attr.name for attr in fields(ExecutionMetadata)],
        )
        if existing_versions is not None:
            # Fill the revision number by looking in the model's existing
            # versions list.
            df_execs.loc[:, "revision"] = df_execs["version_id"].apply(
                lambda x: "unsaved"
                if x is None
                else (
                    "deleted"
                    if x not in existing_versions["version"].to_numpy()
                    else existing_versions.loc[
                        existing_versions["version"] == x, "revision"
                    ].iloc[0]
                )
            )
            df_execs = df_execs.set_index("date")
        else:
            df_execs = df_execs.set_index("date")
            for e in self.content:
                if hasattr(e, "revision"):
                    df_execs.loc[e.date, "revision"] = e.revision

        return df_execs

    def append(self, element: ExecutionMetadata):
        self.content.append(element)


class VersionNamedFile:
    """:obj:`~alloniamodel.model.AllOnIAModel` objects have some extra files
    associated to them, like the description in a json, or the model in a joblib
    for Seldon to use.

    For each version of the model, there is one of those files, named,
    for version ID 'a1ec...' and the description for example,
    :inlinepython:`"notebooks/model/name/a1ec.../description.json"`.

    In addition to those 'versioned paths', the file corresponding to the
    latest version of the model is also present in the non-persistent bucket,
    under the name :inlinepython:`"notebooks/model/name/description.json"` for
    our previous example.

    This class handles that: you create it giving  a 'base path', which is the
    path of the latest version in the non-persistent bucket, and you can do
    basic file operations like delete, read, save by giving a revision number
    or version ID.
    """

    def __init__(
        self,
        base_path: S3Path,
        persistent: bool,
        object_type: str,
        model_kwargs: dict,
        handle_type: bool = True,
    ):
        """

        Args:
            base_path: For example, "notebooks/model/name/description.json"
            persistent: Whether the versioned paths should be on the persistent
                or non-persistent bucket. The base path is always on the non-
                persistent bucket.
            object_type: str
                To overload autodetect of object type based on its directory.
            handle_type: bool
                To overlead default behavior of autohandeling of special types.
            model_kwargs: dict of "class"
                (must be :obj:`alloniamodel.model.AllOnIAModel`),
                "name" (the model's name), "attribute" (the model's attribute
                that this path's file is supposed to contain) and "load_kwargs"
                (any kwargs to give to :obj:`alloniamodel.model.AllOnIAModel`
                init in addition to "name", "read_only" and
                "ignore_requirements". This is used in case someone is trying to
                get a versioned path that does not exist : we then load the
                model at the given revision/version and make the file from the
                specified "attribute".
        """
        self.base_path = base_path
        self.persistent = persistent
        self.model_kwargs = model_kwargs
        self.object_type = object_type
        self.handle_type = handle_type

    def _is_last_version(self, version: str | None, versions):
        if versions is None:
            versions = self._get_model_versions()
        return version == versions["version"].iloc[-1]

    def _get_model_versions(self):
        return self.model_kwargs["class"].list_versions(
            self.model_kwargs["name"]
        )

    def _get_version_path(self, version: str | None = None):
        if version is None:
            return self.base_path, True, False
        return (
            (self.base_path.parent / version / self.base_path.stem).with_suffix(
                self.base_path.suffix
            ),
            False,
            self.persistent,
        )

    def _copy_new_latest(self, versions=None):
        if versions is None:
            versions = self._get_model_versions()
        new_latest = self.read(
            versions["version"].iloc[-2],
            fix_if_missing=True,
            path_only=True,
            versions=versions,
        )
        if new_latest is not None:
            try:
                S3Path(new_latest, persistent=self.persistent).copy(
                    S3Path(self.base_path, persistent=False)
                )
            except Exception as e:
                logger.warning(
                    f"Could not update latest revision for {self.base_path}:"
                    f" {e}."
                )
                return False
            else:
                return True
        return None

    @format_version
    def rm(
        self,
        rev_or_ver: str | int | None = None,
        versions=None,
        update_latest_if_needed=True,
    ):
        """Removes this object's revisioned path.

        If rev_or_ver is None or -1, removes the file corresponding to
        the latest model on the non-persistent bucket instead.

        If the specified rev_or_ver is a positive number and is the model's
        latest revision, or if it is the model's last version's UUID, replaces
        the file corresponding to the latest model on the non-persistent bucket
        by the file corresponding to the model's second to last version, in
        addition to deleting the versioned path. To do that it uses
        :obj:`~_copy_new_latest`.

        If the specified rev_or_ver matches the model's last remaining version,
        also deletes the file corresponding to the latest model on the
        non-persistent bucket.
        """
        (
            versioned_path,
            version_unspecified,
            persistent,
        ) = self._get_version_path(rev_or_ver)
        if (
            self._is_last_version(rev_or_ver, versions=versions)
            and not version_unspecified
            and update_latest_if_needed
        ):
            # versions are provided if we reach this point, as
            # _is_last_revision will always be False otherwise.
            if len(versions.index) == 1:
                # We are actually deleting the last revision, so also delete the
                # base path file on the non-persistent bucket
                if error := try_delete(
                    S3Path(self.base_path, persistent=False),
                    "rm",
                ).errors:
                    logger.warning(f"{error[0]['code']}, {error[0]['message']}")
            else:
                # If the revision was not None or -1, but matched the last
                # revision, replace the current 'latest' file by the
                # 'new latest'.
                self._copy_new_latest(versions=versions)

        if error := try_delete(
            S3Path(versioned_path, persistent=persistent),
            "rm",
        ).errors:
            logger.warning(f"{error[0]['code']}, {error[0]['message']}")

    @format_version
    def write(
        self,
        rev_or_ver: str | int | None = None,
        content=None,
        copy_to_latest: bool = True,
        versions: pd.DataFrame | None = None,
    ) -> dict:
        """Write something to the appropriated revisioned path.

        Args:
            rev_or_ver: revision number or version ID. If None or -1, will
                create the file corresponding to the latest model on the
                non-persistent bucket.
            content: what to write in the file
            copy_to_latest: If True and if the rev_or_ver is not None or -1, and
                is the model's latest version, will recall this method with
                rev_or_ver=None to create the file corresponding to the latest
                model on the non-persistent bucket.
            versions: existing model's versions. If not specified, will be
                recreated from S3.
        """
        (
            versioned_path,
            version_unspecified,
            persistent,
        ) = self._get_version_path(rev_or_ver)
        key_name = f"version: {'latest' if rev_or_ver is None else rev_or_ver}"
        results = {
            key_name: S3Path(
                versioned_path,
                persistent=persistent,
                object_type=self.object_type,
            ).write(content)
        }
        if (
            not version_unspecified
            and copy_to_latest
            and self._is_last_version(rev_or_ver, versions=versions)
        ):
            results.update(self.write(None, content, False, versions=versions))

        return results

    @format_version
    def read(
        self,
        rev_or_ver: str | int | None = None,
        fix_if_missing: bool = True,
        path_only: bool = False,
        versions=None,
    ) -> None | dict | S3Path:
        """Reads the content of the file matching the required revision. If None
        or -1, uses the one on the non-persistent bucket corresponding to the
        model's latest revision.

        Args:
            rev_or_ver: revision number or version ID.
            fix_if_missing: If the file corresponding to rev_or_ver does not
                exist, it is created: if the rev_or_ver is None or -1,
                :obj:`~_copy_new_latest` is called. Else, the
                :obj:`~alloniamodel.model.AllOnIAModel` is loaded with the
                specified
                version, and the approriate attribute is read from it using
                :obj:`~model_kwargs`, and written using :obj:`write_kwargs`
            path_only: Does not return the file content, just the path. Still
                checks the file existence and tries to fix it if not present
                and if fix_if_missing is True.
            versions: existing model's versions. If not specified, will be
                recreated from S3.


        Returns:
            The revisioned path if :inlinepython:`path_only=True`, else its
            content.
        """
        (
            versioned_path,
            version_unspecified,
            persistent,
        ) = self._get_version_path(rev_or_ver)

        # The file we are looking for is missing : try to create it if possible
        # and if not specified otherwise.
        if not self.exists(rev_or_ver, versions=versions):
            if not fix_if_missing:
                logger.warning(
                    f"Can not load {versioned_path} revision-named file"
                    " not found."
                )
                return None
            # The file is missing : we need to load the model at this
            # version to make the file. rev_or_ver is now forced to be the
            # version by the format_version decorator.
            model = self.model_kwargs["class"](
                self.model_kwargs["name"],
                version=rev_or_ver,
                fast=True,
                **self.model_kwargs.get("load_kwargs", {}),
            )
            value = getattr(model, self.model_kwargs["attribute"])
            if value is not None:
                self.write(rev_or_ver, value, True, versions=versions)
                return versioned_path if path_only else value
            logger.warning(
                f"Could not load {self.model_kwargs['attribute']} from"
                " binary file : value is None."
            )
            return None
        return (
            versioned_path
            if path_only
            else S3Path(
                versioned_path,
                persistent=persistent,
                object_type=self.object_type,
                handle_type=self.handle_type,
            ).read()
        )

    @format_version
    def exists(
        self,
        rev_or_ver: str | int | None = None,
        versioned: bool = False,
        versions=None,  # noqa: ARG002 keep it, used by the check_valid_revision decorator
    ):
        """Returns True if there is a file at the given path for the given
        revision.

        Args:
            rev_or_ver: The revision number of version ID to use. The user can
                give a numner, a string or None, but the decorator
                'format_revision' will transform it into a valid version UUID
                if it is a number.
            versioned: If True, ignores the file on the non-persistent
                bucket corresponding to the model's latest revision.
            versions: existing model's versions. If not specified, will be
                recreated from S3.
        """
        (
            versionned_path,
            version_unspecified,
            persistent,
        ) = self._get_version_path(rev_or_ver)

        if version_unspecified and versioned:
            return False

        return S3Path(versionned_path, persistent=persistent).is_file()


def get_data_sample(
    data: np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None,
):
    if isinstance(data, (pd.DataFrame, pd.Series)):
        return data.head(5).to_numpy().tolist()
    if isinstance(data, np.ndarray):
        return data[:5].tolist()
    return "No example to display"
