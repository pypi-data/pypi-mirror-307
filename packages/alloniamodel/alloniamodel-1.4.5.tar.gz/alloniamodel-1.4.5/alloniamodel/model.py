from __future__ import annotations

import importlib.metadata
import inspect
import logging
import os
import platform
import signal
import sys
from copy import copy, deepcopy
from datetime import datetime
from typing import Any, Callable, ClassVar

import numpy as np
import pandas as pd
from allonias3 import S3Path
from allonias3.helpers.getattr_safe_property import getattr_safe_property
from allonias3.helpers.responses import DeleteResponse
from sklearn.model_selection import train_test_split
from typeguard import typechecked

from .checker import _check_kwargs
from .decorator import (
    ReadyDecorator,
    _limit_arguments,
    _record_execution,
    classproperty,
    convert_self_kwarg,
)
from .enums import FeatEngSetToUse
from .errors import (
    NotReadyError,
    ReadOnlyError,
    VersionNotFoundError,
    both_x_and_upper_x,
    feat_eng_return_err,
    health_check_failed_err,
    invalid_req_err,
    invalid_revision_err,
    invalid_test_validate_value_err,
    lockfile_exists_err,
    model_binary_not_fount_err,
    model_should_implement_err,
    raw_or_observed_err,
    set_size_err,
    version_and_revision_err,
)
from .utils import (
    BackwardCompatibleObject,
    DataHandler,
    Description,
    ExecutionList,
    SpecialDataFormat,
    VersionNamedFile,
    _Requirement,
    _Validator,
    check_valid_revision,
    check_valid_version,
    format_assets_history,
    get_data_sample,
    get_open_by,
    get_type,
    get_variable,
    reshape,
    try_delete,
)
from .variables import Variables

logger = logging.getLogger("alloniamodel.model")


class AllOnIAModel(BackwardCompatibleObject):
    """
    Assumed learning pipeline is as follows:
        1. Load raw data.
        2. Run the raw data through a feature engineering function.
        3. Split the feature engineered data into train, validation and test
           sets.
        4. train the model on predictive variables. Depending on the model type,
           it can be to predict some target variables.
        5. Evaluate the performance using the validation and test sets.

    Assumed prediction pipeline is as follows:
        1. Load observed data.
        2. Run the observed data through the same feature engineering function
           as the raw data.
        3. Predict using the predictive variables specified in the learning
           phase.
        4. Post-process the predictions to make them human-readable.

    Learning pipeline in details:
        See :ref:`pipeline_learn`.

    Prediction pipeline in details:
        See :ref:`pipeline_predict`.

    See Also:
        * :ref:`pipeline_steps`
        * :ref:`data_input`
        * :ref:`data_retention`
        * :obj:`root`
        * :obj:`save`

    .. NOTE: Please document all `getattr_safe_property` attributes below using
      the `.. attribute::` directive to ensure they appear in the documentation,
      and DO NOT comment them in their definition directly

    .. attribute:: raw_set

       The set of raw data on which to learn.

       Should contain both predictive and target variables. Set it by giving a
       :obj:`~numpy.ndarray`, :obj:`~pandas.DataFrame`, a :obj:`str` or a
       collection of :obj:`str` to where the data is, the AllOnIAModel class
       will load the data internally.

       :type: Union[
        ~numpy.ndarray, ~pandas.DataFrame, ~pandas.Series, SpecialDataFormat,
        None]

    .. attribute:: observations_set

       The set on which to make an actual
       prediction. Should contain only predictive variables. Set it by giving a
       :obj:`~numpy.ndarray`, :obj:`~pandas.DataFrame`, a :obj:`str` or a
       collection of :obj:`str` to where the data is, the AllOnIAModel class
       will load the data internally.

       :type: Union[
        ~numpy.ndarray, ~pandas.DataFrame, ~pandas.Series, SpecialDataFormat,
        None]

    .. attribute:: derived_set

       Result of :obj:`~feature_engineering_function` applied on
       :obj:`raw_set`.

       :type: Union[
        ~numpy.ndarray, ~pandas.DataFrame, ~pandas.Series, SpecialDataFormat,
        None]

    .. attribute:: health_check_set

       An optional set of data, similar to :obj:`raw_set` in its structure,
       but with a reduced number of entries.

       Will be used by :obj:`health_check` : the full learning and prediction
       pipeline will run on it, to check that everything is in order in the
       model. So it must be small enough for the pipeline to run fast.

       Should contain both predictive and target variables. Set it by giving a
       :obj:`~numpy.ndarray`, :obj:`~pandas.DataFrame`, a :obj:`str` or a
       collection of :obj:`str` to where the data is, the AllOnIAModel class
       will load the data internally.

       :type: Union[
        ~numpy.ndarray, ~pandas.DataFrame, ~pandas.Series, SpecialDataFormat,
        None]

    .. attribute:: health_check_observations_set

       An optional set of data, similar to :obj:`observations_set` in its
       structure, but with a reduced number of entries.

       Will be used by :obj:`health_check` : the prediction
       pipeline will run on it, to check that everything is in order in the
       model. So it must be small enough for the pipeline to run fast.

       Should contain only predictive variables. Set it by giving a
       :obj:`~numpy.ndarray`, :obj:`~pandas.DataFrame`, a :obj:`str` or a
       collection of :obj:`str` to where the data is, the AleiaModel class
       will load the data internally.

       :type: Union[
        ~numpy.ndarray, ~pandas.DataFrame, ~pandas.Series, SpecialDataFormat,
        None]

    .. attribute:: intermediary_save_path

        Path where all the intermediary data (derived, train, test...)
        created by this instance can be saved:
        ':obj:`root`/dataset/:obj:`name`/intermediary_data/'.

        :type: ~allonias3.s3_path.S3Path

    .. attribute:: seldon_implementation

        Returns the Seldon implementation matching this model, or None if the
        model is not defined.

        Currently, packages that have a supported implementations are sklearn
        tensorflow and xgboost. If the model is from a package with no known
        Seldon implementation, 'CUSTOM_INFERENCE_SERVER' is returned.

        :type: str | None

    .. attribute:: read_only

        The user can choose to open the model in read-only mode. In that case
        the presence of the model's lockfile will not prevent the model from
        opening, but no saving operation will be done, be it the model itself or
        its data.

        If the model is not open in read-only mode and the lockfile exists, the
        model will raise :obj:`utils.ReadOnlyError`.

        :type: bool

    .. attribute:: open_by

        'track', 'project' and 'user' ID running this function, and in
        which 'file'.

        :type: bool

    .. attribute:: open_by_history

        History of when this model was opened and closed and by which .py
        or .ipynb file.

        :type: dict

    .. attribute:: related_assets

        All assets that ever used this model, indexed by the last time each
        index used the model.

        :type: ~pandas.DataFrame

    .. attribute:: open_at

        timestamp when the object was instanciated.

        :type: str

    .. attribute:: description

        Description of the model, made partially by the user, partially
        deduced from attributes.

        The user must manually specify some entries in the description through
        :obj:`update_description`.

        :type: dict

    .. attribute:: revision

        The current model's revision. 0 if the model has not been saved yet

        :type: int

    .. attribute:: feature_engineering_summary

        Returns a :obj:`~pandas.DataFrame` indexes by dates, of all the
        runs of :obj:`feature_engineering` made by this instance, containing
        information like runtime, used arguments, ...

        :type: ~pandas.DataFrame

    .. attribute:: splits_summary

        Returns a :obj:`~pandas.DataFrame` indexes by dates, of all the
        runs of :obj:`train_val_test_split` made by this instance, containing
        information like runtime, used arguments, ...

        :type: ~pandas.DataFrame

    .. attribute:: learnings_summary

        Returns a :obj:`~pandas.DataFrame` indexes by dates, of all the
        runs of :obj:`learn` made by this instance, containing
        information like runtime, used arguments, ...

        :type: ~pandas.DataFrame

    .. attribute:: trainings_summary

        Returns a :obj:`~pandas.DataFrame` indexes by dates, of all the
        runs of :obj:`train` made by this instance, containing
        information like runtime, used arguments, ...

        :type: ~pandas.DataFrame

    .. attribute:: validations_summary

        Returns a :obj:`~pandas.DataFrame` indexes by dates, of all the
        runs of :obj:`validate` made by this instance, containing
        information like runtime, used arguments, ...

        :type: ~pandas.DataFrame

    .. attribute:: tests_summary

        Returns a :obj:`~pandas.DataFrame` indexes by dates, of all the
        runs of :obj:`test` made by this instance, containing
        information like runtime, used arguments, ...

        :type: ~pandas.DataFrame

    .. attribute:: applies_summary

        Returns a :obj:`~pandas.DataFrame` indexes by dates, of all the
        runs of :obj:`apply` made by this instance, containing
        information like runtime, used arguments, ...

        :type: ~pandas.DataFrame

    .. attribute:: predicts_summary

        Returns a :obj:`~pandas.DataFrame` indexes by dates, of all the
        runs of :obj:`predict` made by this instance, containing
        information like runtime, used arguments, ...

        :type: ~pandas.DataFrame

    .. attribute:: postprocesses_summary

        Returns a :obj:`~pandas.DataFrame` indexes by dates, of all the
        runs of :obj:`postprocess` made by this instance, containing
        information like runtime, used arguments, ...

        :type: ~pandas.DataFrame
    """

    _seldon_implementations: ClassVar = {
        "sklearn": "SKLEARN_SERVER",
        "xgboost": "XGBOOST_SERVER",
        "tensorflow": "TENSORFLOW_SERVER",
    }

    _seldon_model_suffixes: ClassVar = {
        "SKLEARN_SERVER": ".joblib",
        "XGBOOST_SERVER": ".bst",
    }

    root: S3Path = S3Path(
        "notebooks", handle_type=True, verbose=False, persistent=True
    )
    """Root path of the file system. If it does not exist yet, a *model*
    directory will be created in it when needed. Anything saved by an instance
    of this class will be contained inside the :obj:`root`/model/:obj:`name`/
    directory.
    """
    save_intermediary_data: bool = False
    """see :ref:`data_retention`
    """
    _common_model_dir = "model"
    """Where all models are saved. Will be appended to :obj:`root` to
    create :obj:`_model_root_path`."""
    _model_root_path: S3Path = None
    """Path where all the models created by this class will be saved :
    ':obj:`root`/model/'.
    """
    _path_makers: ClassVar = {
        "directory": lambda root, name: root / name,
        "description": lambda root, name: root / name / "description.json",
        "open_by": lambda root, name: S3Path(
            root / name / "open_by.json", persistent=False
        ),
        "binary": lambda root, name: root / name / "model.aleiamodel",
        "lock": lambda root, name: S3Path(
            (root / name / "model.aleiamodel").with_suffix(".lock"),
            persistent=False,
        ),
    }
    """Lambda functions to create a model's various path based on its name
    and on :obj:`~_common_model_dir`.
    """

    _valid_set_names = ("train", "validation", "test", "observations")
    """Sets on which predicting is possible.
    """

    datasets = (
        "_raw_set",
        "_derived_set",
        "_train_set",
        "_validation_set",
        "_test_set",
        "_observations_set",
        "_derived_observations_set",
        "_postprocessed_predictions_set",
        "_health_check_set",
        "_health_check_observations_set",
    )
    """Names of all datasets that can exist in the model."""

    triggers_health_check = (
        "raw_set",
        "observations_set",
        "predictive_variables",
        "target_variables",
        "model_class",
        "model",
        "train_val_test_split_function",
        "_validation_set_size",
        "_test_set_size",
        "feature_engineering_function",
        "compute_metrics_function",
        "postprocess_function",
    )
    """Any attribute listed here will, upon modification, tells the AllOnIAModel
    object that it should rerun its health check when :obj:`health_check` is
    called, as any modification of one of those attributes can impact the
    learning or prediction pipeline."""

    _forbidden_in_name: ClassVar = {
        " ": "Model name cannot contain blanks.",
        "\t": "Model name cannot contain blanks.",
        "\n": "Model name cannot contain blanks.",
        "#": "Model name cannot contain Python's comment symbol '#'.",
        os.path.sep: f"Model name cannot contain path separator {os.path.sep}.",
        os.pathsep: f"Model name cannot contain path separator {os.pathsep}.",
    }
    """The keys in the dictionary are forbidden in any model name."""

    _ignored_packages = ("ipykernel", "jupyter", "IPython", "debugpy")
    """Ignore some packages from requirements. Mostly packages related to
    Jupyter : we want to be able to load AllOnIAModels in Jobs, which do not
    have Jupyter installed."""

    _kwargs_dispatch_dict: ClassVar = {
        "health_check": (
            "model_kwargs",
            "feature_engineering_kwargs",
            "train_val_test_split_kwargs",
            "fit_kwargs",
            "predict_for_metrics_kwargs",
            "metrics_kwargs",
            "predict_kwargs",
            "postprocess_kwargs",
        ),
        "learn": (
            "model_kwargs",
            "feature_engineering_kwargs",
            "train_val_test_split_kwargs",
            "fit_kwargs",
            "predict_for_metrics_kwargs",
            "metrics_kwargs",
        ),
        "evaluate": ("predict_for_metrics_kwargs", "metrics_kwargs"),
        "apply": (
            "feature_engineering_kwargs",
            "predict_kwargs",
            "postprocess_kwargs",
        ),
    }
    """Those are the allowed keyword arguments and the associated methods
    to which they can be passed."""
    _execution_lists: ClassVar = [
        "feature_engineering_execs",
        "split_execs",
        "learn_execs",
        "train_execs",
        "validate_execs",
        "test_execs",
        "apply_execs",
        "predict_execs",
        "postprocess_execs",
    ]
    """All instances of :obj:`utils.ExecutionList` that the object
    will define. Declared here instead of in :inlinepython:`__init__` because it
    helps in `:obj:~_update_execution_lists_versions` later.

      * feature_engineering_execs: list of all the executions of the
        :obj:`feature_engineering` method
      * split_execs: list of all the executions of the
        :obj:`train_val_test_split` method
      * learn_execs: list of all the executions of the :obj:`learn` method
      * train_execs: list of all the executions of the :obj:`train` method
      * validate_execs: list of all the executions of the :obj:`validate`
        method
      * test_execs: list of all the executions of the :obj:`test` method
      * apply_execs: list of all the executions of the :obj:`apply` method
      * predict_execs: list of all the executions of the :obj:`predict` method
      * postprocess_execs: list of all the executions of the :obj:`postprocess`
        method
    """

    # Private or protected class methods

    @classmethod
    def _make_paths(cls, name: str, which=None) -> list[S3Path]:
        if which is not None and isinstance(which, str):
            which = (which,)
        return (
            [
                path(cls.model_root_path, name)
                for path in cls._path_makers.values()
            ]
            if not which
            else [cls._path_makers[w](cls.model_root_path, name) for w in which]
        )

    @classmethod
    def _make_seldon_path(cls, name: str, path: S3Path) -> VersionNamedFile:
        """See :obj:`alloniamodel.utils.VersionNamedFile`"""
        return VersionNamedFile(
            path,
            object_type="model",
            persistent=False,
            handle_type=False,
            model_kwargs={"class": cls, "name": name, "attribute": "model"},
        )

    @classmethod
    def _make_description_path(
        cls, name: str, path: S3Path
    ) -> VersionNamedFile:
        """See :obj:`alloniamodel.utils.VersionNamedFile`"""
        return VersionNamedFile(
            path,
            object_type="unknown",
            persistent=True,
            handle_type=True,
            model_kwargs={
                "class": cls,
                "name": name,
                "attribute": "description",
                "load_kwargs": {"load_description": False},
            },
        )

    @classmethod
    def _delete_revision(
        cls, name: str, revision: int
    ) -> DeleteResponse | tuple[DeleteResponse, DeleteResponse]:
        """Deletes one revision of the model's pickle file. If it was the only
        existing revision, calls :obj:`_delete_all`.

        Will also delete the associated Seldon file and description file
        versions.

        Args:
            name: The name of the model to delete
            revision: Revision number to delete.
        """

        model_binary_path, description_path = cls._make_paths(
            name, ("binary", "description")
        )
        str_model_binary = str(model_binary_path)

        versions = cls.list_versions(name)

        try:
            revision, version, _ = check_valid_revision(
                revision, versions, name
            )
        except (VersionNotFoundError, ValueError) as error:
            error = str(error)
            logger.warning(error)
            return DeleteResponse(
                {
                    "Errors": {
                        "Key": str_model_binary,
                        "VersionId": "",
                        "Code": "FileNotFoundError",
                        "Message": error,
                    },
                }
            )

        if len(versions.index) == 1:
            return cls._delete_all(name)

        for suffix in cls._seldon_model_suffixes.values():
            seldon_path = cls._make_seldon_path(
                name, model_binary_path.with_suffix(suffix)
            )
            if seldon_path.exists(version, versions=versions):
                seldon_path.rm(version, versions=versions)
        cls._make_description_path(name, description_path).rm(
            version, versions=versions
        )

        return try_delete(
            model_binary_path,
            "rm",
            version_id=version,
        )

    @classmethod
    def _delete_all(cls, name: str) -> tuple[DeleteResponse, DeleteResponse]:
        """Deletes all files corresponding to this model.

        Args:
            name: The name of the model to delete

        """
        model_directory = cls._make_paths(name, ("directory",))[0]
        return (
            try_delete(
                model_directory,
                "rmdir",
                recursive=True,
            ),
            try_delete(
                S3Path(model_directory, persistent=False),
                "rmdir",
                recursive=True,
            ),
        )

    @classmethod
    def _ignored_module(cls, module: str):
        for ignored_module in cls._ignored_packages:
            if module.startswith(ignored_module):
                return True
        return False

    @classmethod
    def _get_imported_packages(
        cls, include_python: bool = False
    ) -> list[_Requirement]:
        """Returns the list of currently imported packages using
        :obj:`utils._Requirement`. Will include the current
        Python version as a requirement if asked."""
        requirements = [
            _Requirement(module.metadata["Name"], module.version)
            for module in importlib.metadata.distributions()
            if not cls._ignored_module(module.metadata["Name"])
        ]
        if include_python:
            requirements.append(
                _Requirement("Python", platform.python_version())
            )
        return requirements

    @classmethod
    def _load(
        cls,
        model_binary_path: S3Path,
        name: str,
        version: str | None = None,
        revision: int | None = None,
        ignore_requirements: bool = True,
        load_description: bool = True,
    ) -> AllOnIAModel:
        """Loads the object from disk.

        Called by :obj:`__new__`, do not call it yourself.

        When creating a AllOnIAModel object, if the file
        ':obj:`root`/model/:obj:`name`/model.aleiamodel' exists,
        :obj:`__new__` calls this method to load the object, and :obj:`__init__`
        is skipped.
        In that case, a check can be made on the requirements specified in the
        pickled object and the currently installed packages, raising
        :obj:`ModuleNotFoundError` if any package is missing (can be activated
        with `ignore_requirements=True`).

        The required version or revision is loaded. If None, raises
        :obj:`errors.VersionNotFoundError`.

        Will NOT load the description file : :obj:`description` is already
        present in the loaded pickle file.

        Only path(s) to the :obj:`raw_set`, :obj:`observations_set`,
        :obj:`health_check_set` and :obj:`health_check_observations_set` are
        retrieved, all other data (validation
        and test sets, predictions...) is lost. It can still be present in
        ':obj:`root`/model/:obj:`name`/intermediary_data/' if
        :obj:`save_intermediary_data` was :inlinepython:`True` when :obj:`save`
        was called, but they are not accessible through the loaded instance.

        Raises:
            ModuleNotFoundError: if any package is missing in the current
                running environment compared to the one used when the loaded
                object was pickled.
            VersionNotFoundError: if the specified revision or version is not
                found.
        """
        versions = AllOnIAModel.list_versions(name)

        if revision is not None:
            revision, version, creation_date = check_valid_revision(
                revision, versions, name
            )
        else:
            revision, version, creation_date = check_valid_version(
                version, versions, name
            )

        logger.info(
            f"Loading model {name} with version {version}"
            f" created on {creation_date}.",
        )

        obj = model_binary_path.read(
            version_id=version,
            raise_if_unpickle_fails=True,
        )
        if obj.__class__.__name__ == "AleiaModel":
            logger.warning(
                "Loading deprecated AleiaModel object. Not everything might "
                "work as expected. Consider recreating a new model"
                " using AllOnIAModel."
            )
        elif not isinstance(obj, AllOnIAModel):
            raise TypeError(
                f"The model's file contained a {type(obj)}, not an AllOnIAModel"
            )
        obj._version_id = version
        obj._update_execution_lists_versions()

        if (
            load_description
            and (
                description := cls._make_description_path(
                    name, cls._make_paths(name, ("description",))[0]
                ).read(
                    # If the associated description file does not exist, just
                    # use the pickled description
                    version,
                    fix_if_missing=False,
                    versions=versions,
                )
            )
            is not None
        ):
            obj._description.dict = description

        obj._name = name

        if not ignore_requirements:
            modules = cls._get_imported_packages()
            obj.compare_requirements(modules)

        for dataset_name in obj.datasets:
            getattr(obj, dataset_name).attached_to = obj
        for prediction_name in obj._predictions:
            obj._predictions[prediction_name].attached_to = obj
        # To trigger Description update
        obj._predictions = obj._predictions
        return obj

    # Public class methods

    @classproperty
    def model_root_path(cls) -> S3Path:  # noqa: N805
        cls._model_root_path = cls.root / cls._common_model_dir
        return cls._model_root_path

    @classmethod
    @typechecked
    def get_description(
        cls,
        name: str,
        revision_or_version: None | int | str = None,
        path_only: bool = False,
        fix_if_missing: bool = True,
        _versions: pd.DataFrame | None = None,
    ) -> None | dict | S3Path:
        """Returns the description of one model, without creating the model
        object. This is quicker.

        Args:
            name: The name of the model
            revision_or_version: which revision or version to get the
                description for. None or -1
                means the latest revision. If the corresponding revision file
                is not found for the description, the model is loaded anyway
                and the description extracted from it to create the file, unless
                'fix_if_missing' is False.
            path_only: see :obj:`utils.VersionNamedFile.read`.
            fix_if_missing: see :obj:`utils.VersionNamedFile.read`.
            _versions: for internal calls only

        Returns:
            The model description, or just its path, or None if the specified
            revision/version was not found.
        """
        # skips revision checks to save time
        return cls._make_description_path(
            name, cls._make_paths(name, ("description",))[0]
        ).read(
            revision_or_version,
            path_only=path_only,
            fix_if_missing=fix_if_missing,
            versions=_versions,
        )

    @classmethod
    def update_description(
        cls,
        name: str,
        entries: dict[str, str],
        revision: int = -1,
    ) -> dict | None:
        """Updates entries in the model's description file.

        Only entries listed in
        :obj:`utils.Description.VALID_USER_ENTRIES` will be
        updated, the others will be ignored.

        Args:
            name: The name of the model to update the description of
            revision: which revision to update the description for. -1 means the
                latest revision (default).
            entries: keys must be in
                :obj:`utils.Description.VALID_USER_ENTRIES`,
                values are the descriptions (:obj:`str`).

        Returns:
            The updated description
        """
        versions = cls.list_versions(name)
        if len(versions.index) == 0:
            return None
        revision, version, _ = check_valid_revision(revision, versions, name)
        description = cls.get_description(
            name, revision, fix_if_missing=False, _versions=versions
        )
        if description is None:
            return None
        description = Description(None, description)
        if description.update_user_entries(entries):
            cls._make_description_path(
                name, cls._make_paths(name, ("description",))[0]
            ).write(
                version,
                description.dict,
            )
        return description.dict

    @classmethod
    def get_opening_history(cls, name: str) -> None | dict:
        """Returns the history of who opened the model and when, if the model
        exists.

        Args:
            name: The name of the model

        Returns:
            None if the model has no openning history, or a dict with keys being
            opening timstamps, and values being another dict containing
            information about who opened the model and when it got closed again,
            and a path to the file.
        """
        open_by = cls._make_paths(name, ("open_by",))[0]
        if not open_by.is_file():
            logger.warning(
                f"AllOnIAModel '{name}' does not have an openning history."
            )
            return None
        return open_by.read()

    @classmethod
    def get_related_assets(cls, name: str) -> pd.DataFrame:
        """All assets that ever used this model, indexed by the last time each
        index used the model.
        """
        return format_assets_history(cls.get_opening_history(name))

    @classmethod
    def unlock(
        cls,
        name: str,
    ) -> DeleteResponse:
        """Deletes the lockfile corresponding to this model.

        Args:
            name: The name of the model to delete
        """
        response = try_delete(
            cls._make_paths(name, ("lock",))[0],
            "rm",
        )
        logger.info(
            f"Unlocked model {name}. It is now available for other users in"
            f" edition mode.",
        )
        return response

    @classmethod
    def delete(
        cls,
        name: str,
        revision: int | None = None,
    ) -> tuple[DeleteResponse, DeleteResponse] | DeleteResponse:
        """Deletes all files corresponding to this model (except datasets, if
        any), or just the pickle, Seldon and description files of one specific
        revision.
        If this deleted revision was the last one, deletes the model entierly.

        Args:
            name: The name of the model to delete
            revision: Revision number to delete.
        """
        if revision is not None and revision == 0:
            raise invalid_revision_err()

        return (
            cls._delete_revision(name, revision)
            if revision is not None
            else cls._delete_all(name)
        )

    @classmethod
    def locked(cls, name: str) -> bool:
        """Returns True if the model corresponding to the given name is locked.
        Does not instantiate the model, just checks for the existence of the
        lockfile.
        """
        return cls._make_paths(name, ("lock",))[0].is_file()

    @classmethod
    @typechecked
    def list_versions(cls, model: AllOnIAModel | str) -> pd.DataFrame:
        """Lists all S3 versions of the given model .aleiamodel file.

        It is a class method to allow listing versions of models without
        creating the corresponding instances.

        Args:
            model: Either the model name, or the model object directly.

        Returns:
             pd.DataFrame: All available versions, sorted by increasing creation
                date.
        """
        if isinstance(model, str):
            model_binary_path = cls._make_paths(model, ("binary",))[0]
            if not model_binary_path.is_file():
                return pd.DataFrame(
                    columns=["date", "version", "revision"]
                ).set_index("date")
            versions = model_binary_path.versions(details=True)
        else:
            versions = model.binary_path.versions(details=True)

        versions = (
            pd.DataFrame(
                columns=["date", "version", "revision"],
                data=[
                    (
                        obj["last_modified"],
                        obj["version_id"],
                        0,
                    )
                    for obj in versions.successes
                ],
            )
            .set_index("date")
            .sort_index()
        )
        versions.loc[:, "revision"] = np.arange(1, len(versions.index) + 1)
        return versions

    # Magic methods

    def __getnewargs__(self):
        """When unpickling the object, need to provide :obj:`__new__` with a
        name"""
        return ("",)

    def __new__(  # noqa: C901, PLR0912, PLR0913, PLR0915
        cls,
        name: str,
        version: str | None = None,
        revision: int | None = None,
        read_only: bool = False,
        must_exist: bool = False,
        do_not_log_open: bool = False,
        ignore_requirements: bool = False,
        override_lock: bool = False,
        fast: bool = False,
        load_description: bool = True,
        allow_load_fail: bool = True,
    ):
        """Will load the pickled object if the file exists, which will skip
        :obj:`__init__`, else sets the new object's paths and continues
        to :obj:`__init__`.
        In both cases, sets :obj:`open_by` value to the current executing file
        name.

        If the specified version does not exist, will load the latest one.

        If the model is already open somewhere (the lockfile exists), the model
        will be read-only.
        """
        if not name:
            # Happens when AllOnIAModel._load just unpickled the file :
            # then no arguments are passed to __new__
            obj = object.__new__(cls)
            obj._open_by = get_open_by() if not fast else {}
            return obj

        if fast:
            read_only = True
            ignore_requirements = True
            version = None
            revision = None

        for key in cls._forbidden_in_name:
            if key in name:
                raise ValueError(cls._forbidden_in_name[key])

        model_binary_path, lockfile = cls._make_paths(name, ("binary", "lock"))
        # Cast into a new S3Path that is NOT persistent
        lockfile = S3Path(
            lockfile,
            persistent=False,
            handle_type=True,
            verbose=False,
            object_type="unknown",
        )
        locked_to = None

        exists = model_binary_path.is_file() if not fast else True
        if revision is not None and version is not None:
            raise version_and_revision_err()
        if not exists and (
            must_exist or (revision is not None or version is not None)
        ):
            raise model_binary_not_fount_err(model_binary_path)

        if not read_only:
            if lockfile.is_file():
                if override_lock:
                    logger.warning(f"Overriding lock for model {name}.")
                else:
                    raise lockfile_exists_err(name, lockfile)
            # If we intend to write something on disk regarding this model, lock
            # it so that no one else can while we are working.
            # The lockfile will be deleted when the program ends or when the
            # object is deleted.

            lockfile.write(f"{datetime.now()}: locked by {get_open_by()}")
            locked_to = lockfile

        if exists:
            try:
                obj = cls._load(
                    model_binary_path,
                    name,
                    version=version,
                    revision=revision,
                    ignore_requirements=ignore_requirements,
                    load_description=load_description,
                )
            except Exception as error:
                # If loading failed, we do not want to keep the model locked for
                # nothing.
                try:
                    cls.unlock(name)
                except Exception:
                    logger.debug("Not locked, pass")
                if not allow_load_fail:
                    raise error
                logger.warning(
                    f"Failed to load model {name}: "
                    f"{error}. Try again, and if"
                    f" the problem persists, you will have to either"
                    f" check your package versions, or recreate your model"
                    f" from sratch.\n"
                    f" Returning a non-loaded AleiaModel object."
                )
                obj = object.__new__(cls)
                obj._loaded = False
                # Those two are needed by _log_openning so must be created in
                # __new__ and not in __init__
                obj._name = name
                obj._open_by_path = None
            else:
                obj._loaded = True
        else:
            obj = object.__new__(cls)
            obj._loaded = False
            # Those two are needed by _log_openning so must be created in__new__
            # and not in __init__
            obj._name = name
            obj._open_by_path = None

        obj._read_only = read_only
        if read_only:
            obj._locked_to = None
            obj.save_intermediary_data = False
        else:
            obj._locked_to = locked_to
            signal.signal(signal.SIGTERM, obj._release_lock)
            signal.signal(signal.SIGINT, obj._release_lock)
            signal.signal(signal.SIGTERM, obj._log_closing)
            signal.signal(signal.SIGINT, obj._log_closing)

        obj._open_by = get_open_by() if not fast else {}
        obj._open_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        obj._closed_at = None

        if not do_not_log_open and not fast:
            obj._log_openning()

        return obj

    @typechecked
    def __init__(  # noqa: PLR0913, PLR0915
        self,
        name: str,  # noqa: ARG002
        version: str | None = None,  # noqa: ARG002
        revision: int | None = None,  # noqa: ARG002
        read_only: bool = False,
        must_exist: bool = False,  # noqa: ARG002
        do_not_log_open: bool = False,  # noqa: ARG002
        ignore_requirements: bool = False,  # noqa: ARG002
        override_lock: bool = False,  # noqa: ARG002
        fast: bool = False,  # noqa: ARG002
        load_description: bool = True,  # noqa: ARG002
        allow_load_fail: bool = True,  # noqa: ARG002
    ):
        """
        Skipped if the model already exists in the file
        ':obj:`root`/model/:obj:`name`/model.aleiamodel', in which case it is
        loaded from it in :obj:`__new__`.

        Args:
            name: the name of the model, will become the :obj:`name` attribute.
            version: the S3 version of the model to load. If
                None, loads the latest one. One can list all available versions
                for a given model (object or name) through :obj:`list_versions`.
            revision: the revision number of the model to load. If
                None, loads the latest one.
                Note that you can not specify both version and revision.
                Can not be 0. 1 is the first revision, 2 the second, -1 is the
                latest (equivalent to "None"), -2 the second-to-last, etc...
            read_only: The user can choose to open the model in read-only mode.
                If not, the model will create a lockfile to prevent other
                processes to open and modify it (deleted upon object
                destruction). If the lockfile already exists and read-only if
                False, the error :obj:`errors.ReadOnlyError` is
                raised. If read-only is True, no intermediary data will be saved
                and attempting call :obj:`save` the model will also raise
                :obj:`errors.ReadOnlyError`.
                Note that 'read only' means that no changes can be made on the
                S3 files, the object in memory CAN be changed to make quick
                learning/prediction tests in a single notebook.
            must_exist: If True, will raise :obj:`FileNotFoundError` if there is
                no existing version of the model.
            do_not_log_open: If the opening of the model should not be logged.
            ignore_requirements: If True, will load a previously existing model
                even if its requirements do not match the current envirronment.
            override_lock: If True, will ignore the lockfile and load the model
                even if it is open. It will still warn, though.
            fast: If True, model will be read only,
                requirements will be ignored and open will not be logged.
            load_description: If True (default), loads the description from
                the json file associated to the current revision. Else, uses
                the one present in the pickle. Only relevant for non-new models.

        Warns:
            :If the object is loaded from the pickle file and if packages or
             Python itself have different version between the current
             Python environment and the one that created the pickle have
             unmatched versions.
            :If the object is loaded from the pickle file and if packages are
             missing from the current Python environment compared to the one
             when the pickle was created. In that case, the model will likely
             not run, but you can still explore its defined attributes.

        Raises:
            VersionNotFoundError: If specified revision or version was not
                found.
        """
        # Declared here because needed in _log_openning
        if self._loaded:
            # If object just got unpickled, skip __init__
            self._new = False
            return

        self._new = True
        self._directory_path = None
        self._description_path = None
        self._open_by_path = None
        self._binary_path = None
        self._version_named_description_path = None
        self._version_named_seldon_path = None
        self._is_production = False
        self._classes = None
        self._use_latest_data = True
        self._version_id = None
        self._read_only = read_only
        """The user can choose at any time to specify which revision of the
        dataset files needs to be used."""
        self.model_name = None
        """Set automatically when the user defines a model or model class. Can
        also be defined by hand, but is overridden when model or model class is
        defined."""

        self._predictive_variables = Variables.handle_input(("x",))
        self._target_variables = Variables.handle_input(("y",))
        self._fit_function_name = "fit"
        self._predict_function_name = "predict"
        self._validation_set_size = 0.2
        self._test_set_size = 0.2
        self._random_state = None  # for train-test split
        self._validators = []
        self._model = None
        self._model_class = None
        self._seldon_implementation = None

        self._raw_set = DataHandler(self)
        self._derived_set = DataHandler(self)
        self._train_set = DataHandler(self)
        self._validation_set = DataHandler(self)
        self._test_set = DataHandler(self)
        self._observations_set = DataHandler(self)
        self._derived_observations_set = DataHandler(self)
        self._health_check_set = DataHandler(self)
        self._health_check_observations_set = DataHandler(self)

        self._predictions: dict = {
            dataset: DataHandler(self) for dataset in self._valid_set_names
        }
        self._postprocessed_predictions_set = DataHandler(self)

        self._feature_engineering_function = lambda x: x
        self._train_val_test_split_function = train_test_split
        self._compute_metrics_function = lambda _, __=None, **___: {}
        self._postprocess_function = lambda x: x

        self._requirements = self._get_imported_packages(include_python=True)

        for attr in self._execution_lists:
            setattr(self, attr, ExecutionList(self))

        self._input_sample = None
        self._output_sample = None
        self._description = Description(self, {})

        self._rerun_health_check = True
        self._healthy = False

    def __setattr__(self, key, value):
        """Overloaded to automatically update description when some
        attributes are set."""
        super().__setattr__(key, value)
        if key in Description.VALID_AUTO_ENTRIES and hasattr(
            self, "_description"
        ):
            self._description.update_auto_entry(key, self)
        if key in self.triggers_health_check:
            self._rerun_health_check = True

    def __str__(self):
        return f"AllOnIAModel object {self.name}"

    # Private and protected methods

    def _update_execution_lists_versions(self):
        """For each attribute of this model that is of type
        :obj:`utils.ExecutionList`, will set the version id of the
        latest :obj:`utils.ExecutionMetadata` if it is None.
        """
        if not self.version_id:
            return
        for attr in self._execution_lists:
            exec_list = getattr(self, attr)
            for exec_metadata in reversed(exec_list.content):
                if exec_metadata.version_id is not None:
                    break
                exec_metadata.version_id = self.version_id
                break
            # Trigger description update
            setattr(self, attr, exec_list)

    def __check_fit_predict(self, model):
        for method in (self.fit_function_name, self.predict_function_name):
            if method is None:
                continue
            if not hasattr(model, method):
                raise model_should_implement_err(method)

    def _define_set(self, name, value, persist=True):
        attribute_name = f"_{name}_set"
        if isinstance(value, DataHandler):
            setattr(self, attribute_name, value)
        else:
            setattr(
                self,
                attribute_name,
                DataHandler(self, value, name if persist else None),
            )

    @typechecked
    def _set_predictions(
        self,
        set_name: str,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | DataHandler
        ),
    ):
        if not isinstance(pointer, DataHandler):
            pointer = DataHandler(self, pointer, f"{set_name}_predictions")
        self._predictions[set_name] = pointer
        # To trigger Description update
        self._predictions = self._predictions

    def _detect_seldon_implementation(self, the_model):
        return self._seldon_implementations.get(
            the_model.__module__.split(".")[0], "CUSTOM_INFERENCE_SERVER"
        )

    def _log_openning(self):
        if self.open_by_path.is_file():
            content = self.open_by_path.read()
        else:
            content = {}
        content[self._open_at] = {"open_by": self._open_by}
        self.open_by_path.write(content)

    def _log_closing(self, signum, frame):  # noqa: ARG002
        try:
            if self._closed_at is not None:
                return
            if self.open_by_path.is_file():
                content = self.open_by_path.read()
            else:
                return
            if (
                self._open_at not in content
                or "closed_at" in content[self._open_at]
            ):
                return
            self._closed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            content[self._open_at]["closed_at"] = self._closed_at
            self.open_by_path.write(content)
        except Exception as e:
            logger.warning(f"Failed to log closing for one AllOnIAModel: {e}.")

    def _send_summary(self):
        """To be implemented

        Sends execution summary to the validators.
        """

    def _release_lock(self, signum, frame):  # noqa: ARG002
        try:
            if self._locked_to is not None and self._locked_to.is_file():
                errors = try_delete(
                    self._locked_to,
                    "rm",
                ).errors
                if not errors:
                    self._locked_to = None
                else:
                    return errors
        except Exception as error:
            # Can happen when program is closing, there is nothing to do
            # then
            return error

    # Properties

    @property
    @getattr_safe_property
    def directory_path(self) -> S3Path:
        if self._directory_path is None:
            self._directory_path = self._make_paths(self.name, ("directory",))[
                0
            ]
        return self._directory_path

    @property
    @getattr_safe_property
    def intermediary_save_path(self) -> S3Path:
        return self.root / "dataset" / self.name / "intermediary_data"

    @property
    @getattr_safe_property
    def description_path(self) -> S3Path:
        if self._description_path is None:
            self._description_path = self._make_paths(
                self.name, ("description",)
            )[0]
        return self._description_path

    @property
    @getattr_safe_property
    def open_by_path(self) -> S3Path:
        if self._open_by_path is None:
            # Cast to a S3Path that is NOT persistent
            self._open_by_path = S3Path(
                self._make_paths(self.name, ("open_by",))[0],
                persistent=False,
                verbose=False,
                handle_type=True,
                object_type="unknown",
            )
        return self._open_by_path

    @property
    @getattr_safe_property
    def binary_path(self) -> S3Path:
        if self._binary_path is None:
            self._binary_path = self._make_paths(self.name, ("binary",))[0]
        return self._binary_path

    @property
    @getattr_safe_property
    def version_named_description_path(self) -> VersionNamedFile:
        if self._version_named_description_path is None:
            self._version_named_description_path = self._make_description_path(
                self.name, self.description_path
            )
        return self._version_named_description_path

    @property
    @getattr_safe_property
    def version_named_seldon_path(self) -> VersionNamedFile:
        if self._version_named_seldon_path is None:
            self._version_named_seldon_path = self._make_seldon_path(
                self.name,
                self.binary_path.with_suffix(
                    self._seldon_model_suffixes.get(
                        self.seldon_implementation, ".joblib"
                    )
                ),
            )
        return self._version_named_seldon_path

    @property
    @getattr_safe_property
    def seldon_implementation(self) -> str | None:
        return self._seldon_implementation

    @property
    @getattr_safe_property
    def read_only(self) -> bool:
        return self._read_only

    @read_only.setter
    @typechecked
    def read_only(self, value: bool):
        if value is True:
            self._read_only = True
        else:
            logger.warning(
                "Can not manually set read_only to anything else but True"
            )

    @property
    @getattr_safe_property
    def open_by(self) -> dict:
        return self._open_by

    @property
    @getattr_safe_property
    def open_by_history(self) -> dict:
        return self.open_by_path.read() if self.open_by_path.is_file() else {}

    @property
    @getattr_safe_property
    def related_assets(self) -> pd.DataFrame:
        return format_assets_history(self.open_by_history)

    @property
    @getattr_safe_property
    def open_at(self) -> str:
        return self._open_at

    @property
    @getattr_safe_property
    def description(self) -> dict:
        return copy(self._description.dict)

    @typechecked
    def update_model_description(self, entries: dict[str, str]) -> bool:
        """Updates entries in the model's :obj:`description` directly, without
        persisting them to S3.

        Only entries listed in
        :obj:`utils.Description.VALID_USER_ENTRIES` will be
        updated, the others will be ignored.

        Args:
            entries: keys must be in
                :obj:`utils.Description.VALID_USER_ENTRIES`,
                values are the descriptions (:obj:`str`).

        Returns:
            True if something got updated, False otherwise
        """
        return self._description.update_user_entries(entries)

    @property
    def new(self) -> bool:
        """True when the object just got created empty, and not loaded from a
        file."""
        return self._new

    @property
    def name(self) -> str:
        """The model name, used to define its directory where it will be saved :
        ':obj:`root`/model/:obj:`name`/'.
        """
        return self._name

    @property
    def version_id(self) -> str | None:
        """The latest model's version.
        None if the model has not been saved yet.
        """
        return self._version_id

    @property
    @getattr_safe_property
    def revision(self) -> int:
        if not self._version_id:
            return 0
        versions = self.list_versions(self.name)
        return versions.loc[
            versions["version"] == self._version_id, "revision"
        ].iloc[0]

    @property
    def is_production(self) -> bool:
        """The user can set this attribute to True to let others see that this
        AllOnIAModel object is ready for production.

        When trying to set this attribute to True, the AllOnIAModel object will
        call :obj:`health_check`, which needs to pass, otherwise it will raise
        a :obj:`ValueError`.

        Raises:
             ValueError: if trying to set the attribute to True but
                :obj:`health_check` returns False.
        """
        return self._is_production

    @is_production.setter
    @typechecked
    def is_production(self, value: bool):
        if value is True and not self.health_check():
            raise health_check_failed_err()
        self._is_production = value

    @property
    def classes(self) -> tuple | None:
        """When y is a 1-D array and contains integers, booleans or strings,
        we assume we are in a classification problem and save the unique
        values of y as classes. This is done in the :obj:`train` method.
        """
        return self._classes

    @classes.setter
    @typechecked
    def classes(self, value: np.ndarray):
        if len(value) == 0:
            self._classes = None
        python_type = get_type(type(value[0]))
        self._classes = (
            tuple(python_type(v) for v in value)
            if python_type is not object
            else tuple(value)
        )

    @property
    def predictive_variables(self) -> Variables:
        """User-defined variables to learn from. Their given indexes or names
        must be available in the datasets.

        See Also:
            :obj:`variables.Variables`
        """
        return copy(self._predictive_variables)

    @typechecked
    def set_variables(
        self,
        predictive_variables: (
            tuple[int | str, ...]
            | list[int | str]
            | np.ndarray
            | pd.Index
            | Variables
            | pd.DataFrame
            | pd.Series
            | dict
        ),
        target_variables: (
            tuple[int | str, ...]
            | list[int | str]
            | np.ndarray
            | pd.Index
            | Variables
            | pd.DataFrame
            | pd.Series
            | dict
            | None
        ) = None,
    ):
        """Sets the predictive and target (optional)
        :obj:`variables.Variables`.

        Must be done before setting :obj:`model` or :obj:`model_class`.

        Examples:
            .. code-block:: python

                from alloniamodel import AllOnIAModel
                model = AllOnIAModel("iris_classif")
                # One can simply specify columns in a dataframe.
                model.set_variables(
                    ["pred_var_1", "pred_var_2"], ["target_var_1"]
                )
                # Or indexes in a dataframe or np.array.
                model.set_variables([0, 1], [2])
                # For better reporting, one can also specify more information.
                model.set_variables(
                    {
                        "names": ["pred_var_1", "pred_var_2"],
                        "descriptions": ["Patient's age", "Patient's gender"],
                        "types": [int, str]
                    },
                    {
                        "names": ["target_var_1"],
                        "descriptions": ["Survival rate"],
                        "types": [float]
                    },
                )
        """

        self._predictive_variables = Variables.handle_input(
            predictive_variables
        )
        self._target_variables = Variables.handle_input(target_variables)

    @property
    def target_variables(self) -> Variables:
        """User-defined variables to predict. Their given indexes or names
        must be available in the datasets.

        See Also:
            :obj:`variables.Variables`
        """
        return copy(self._target_variables)

    @property
    def validation_set_size(self) -> int | float:
        """Size of the validation set between 0 and 1, as a fraction of the raw
        data set size.

        See Also:
            :obj:`set_set_sizes`
        """
        return self._validation_set_size

    @property
    def test_set_size(self) -> int | float:
        """Size of the test set between 0 and 1, as a fraction of the raw
        data set size.

        See Also:
            :obj:`set_set_sizes`
        """
        return self._test_set_size

    @typechecked
    def set_set_sizes(self, validation: float, test: float):
        """Sets validation and test sizes as fractions of the train set size.

        They can between 0 (included) and 1 (excluded), but the sum of the two
        must be strictly inferior to 1.

        Raises:
            ValuerError: If any size is below 0 or superior or equal to 1
                or of the sum of both sizes is superior or equal to 1.
        """
        if not 0 <= validation < 1:
            raise set_size_err("Validation")
        if not 0 <= test < 1:
            raise set_size_err("Test")

        if test + validation >= 1:
            raise set_size_err()
        self._validation_set_size = float(validation)
        self._test_set_size = float(test)

    @property
    def random_state(self) -> int | None:
        """Random state used in the :obj:`~train_val_test_split_function`."""
        return self._random_state

    @random_state.setter
    @typechecked
    def random_state(self, value: int | None):
        self._random_state = value

    @property
    def validators(self) -> list[_Validator]:
        """list of the persons in charge of validating the model."""
        return copy(self._validators)

    @typechecked
    def add_validators(self, validators: tuple | list):
        for validator in validators:
            self.add_validator(*validator, update_description=False)
        # To trigger description update
        self._validators = self._validators

    @typechecked
    def add_validator(
        self, name: str, email: str, role: str, update_description: bool = True
    ):
        """Adds a validator (a real person in charge of monitoring a model) to
        the AllOnIAModel instance.

        Args:
            name: the validator's name.
            email: the validator's email.
            role: the validator's role.
            update_description: to update the model's description
        """
        validator = _Validator(name, email, role)
        if validator not in self._validators:
            self._validators.append(validator)
            if update_description:
                # To trigger description update
                self._validators = self._validators

    @property
    def fit_function_name(self) -> str:
        """By default, the :obj:`model` is expected to have the *fit* method
        which will be used to fit the model.

        If another function is to be used, the user can specify its name
        through this attribute.
        """
        return self._fit_function_name

    @fit_function_name.setter
    def fit_function_name(self, function_name: str):
        self._fit_function_name = function_name
        if self._model is not None:
            self.__check_fit_predict(self._model)
        elif self._model_class is not None:
            self.__check_fit_predict(self._model_class)

    @property
    def predict_function_name(self) -> str:
        """By default, the :obj:`model` is expected to have the *predict* method
        which will be used to predict from the fitted model.

        If another function is to be used, the user can specify its name
        through this attribute.
        """
        return self._predict_function_name

    @predict_function_name.setter
    def predict_function_name(self, function_name: str):
        self._predict_function_name = function_name
        if self._model is not None:
            self.__check_fit_predict(self._model)
        elif self._model_class is not None:
            self.__check_fit_predict(self._model_class)

    @property
    def model(self) -> Any:
        """An object that must implement the *fit* and *predict* methods (
        or the methods specified by :obj:`fit_function_name` and
        :obj:`fit_function_name`) and remembers its learned hyperparameters.

        The *fit* method should have *X* as first argument.
        If target variables were specified, *y* should be the second argument.
        The *predict* method should have *X* as first argument.
        """
        return copy(self._model)

    @model.setter
    def model(self, model: Any):
        self.__check_fit_predict(model)
        self._model = model
        self._seldon_implementation = self._detect_seldon_implementation(model)
        self.model_name = model.__class__.__name__

    @property
    def model_class(self) -> type:
        """Instead of giving AllOnIAModel the :obj:`model` attribute, which must
        be an instanciated object of a model class, the user can give the class
        itself. This allows the user to do hyperparameter optimisations.

        The :obj:`model` attribute still needs to be instanciated before
        learning, validation, test or prediction. It can be done either by
        giving the *model* key to the *args* and/or *kwargs* arguments of
        :obj:`apply`, in which case those will be used to instanciate the model
        and will set the :obj:`model` attribute, or by doing that by hand :

        >>> from alloniamodel import AllOnIAModel
        >>> model = AllOnIAModel(...)
        >>> model.model_class = ...
        >>> model.model = model.model_class(...)

        If the user calls :obj:`apply`, the :obj:`model` attribute will be
        recreated, even if it was already set. If the user calls  any other
        method involving :obj:`model`, (:obj:`learn`, :obj:`validate`,
        :obj:`test`, :obj:`predict` or :obj:`apply`), the currently instanciated
        model will be used, or an error will raise if it is not istanciated.
        """
        return self._model_class

    @model_class.setter
    def model_class(self, model_class: type):
        self.__check_fit_predict(model_class)
        self._model_class = model_class
        self._seldon_implementation = self._detect_seldon_implementation(
            model_class
        )
        self.model_name = model_class.__name__

    @property
    @getattr_safe_property
    def raw_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        return copy(self._raw_set())

    @raw_set.setter
    @typechecked
    def raw_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("raw", pointer)

    @property
    @getattr_safe_property
    def observations_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        return copy(self._observations_set())

    @observations_set.setter
    @typechecked
    def observations_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("observations", pointer)

    @property
    @getattr_safe_property
    def derived_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        return copy(self._derived_set())

    @derived_set.setter
    @typechecked
    def derived_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("derived", pointer)

    @property
    @getattr_safe_property
    def train_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        return copy(self._train_set())

    @train_set.setter
    @typechecked
    def train_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("train", pointer)

    @property
    @getattr_safe_property
    def validation_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        return copy(self._validation_set())

    @validation_set.setter
    @typechecked
    def validation_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("validation", pointer)

    @property
    @getattr_safe_property
    def test_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        return copy(self._test_set())

    @test_set.setter
    @typechecked
    def test_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("test", pointer)

    @property
    def derived_observations_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        """Result of :obj:`~feature_engineering_function` applied on
        :obj:`~observations_set`.
        """
        return copy(self._derived_observations_set())

    @derived_observations_set.setter
    @typechecked
    def derived_observations_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("derived_observations", pointer)

    @property
    @getattr_safe_property
    def postprocessed_predictions_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        return copy(self._postprocessed_predictions_set())

    @postprocessed_predictions_set.setter
    @typechecked
    def postprocessed_predictions_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("postprocessed_predictions", pointer)

    @property
    @getattr_safe_property
    def health_check_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        return copy(self._health_check_set())

    @health_check_set.setter
    @typechecked
    def health_check_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("health_check", pointer)

    @property
    @getattr_safe_property
    def health_check_observations_set(
        self,
    ) -> np.ndarray | pd.DataFrame | pd.Series | SpecialDataFormat | None:
        return copy(self._health_check_observations_set())

    @health_check_observations_set.setter
    @typechecked
    def health_check_observations_set(
        self,
        pointer: (
            S3Path
            | tuple[S3Path, ...]
            | list[S3Path]
            | np.ndarray
            | pd.DataFrame
            | pd.Series
            | SpecialDataFormat
            | DataHandler
            | None
        ),
    ):
        self._define_set("health_check_observations", pointer)

    @property
    def feature_engineering_function(self) -> Callable:
        """The user can define a feature engineering function. By default, not
        feature engineering is done.

        It takes as input at least 1 argument: a dataset. It should handle both
        the dataset on which learning is done (containing both predictive and
        target variable) and the dataset of observed data on which to predict
        (containing only predictive variables).

        It should return a single :obj:`~numpy.ndarray`,
        :obj:`~pandas.DataFrame` or :obj:`utils.SpecialDataFormat`
        of derived data.
        """
        return self._feature_engineering_function

    @feature_engineering_function.setter
    @_limit_arguments(min_args=1)
    @typechecked
    def feature_engineering_function(self, function: Callable):
        self._feature_engineering_function = function

    @property
    def train_val_test_split_function(self) -> Callable:
        """The user can define a hand-made train-test train_val_test_split
        function. By default, :obj:`~sklearn.model_selection.train_test_split`
        is used.

        It takes as input at least 3 argument : a dataset, a split size and
        a random state. It should only make ONE split.

        It should return 2 :obj:`~numpy.ndarray` or :obj:`~pandas.DataFrame`
        of split data.
        """
        return self._train_val_test_split_function

    @train_val_test_split_function.setter
    @_limit_arguments(min_args=3)
    @typechecked
    def train_val_test_split_function(self, function: Callable):
        self._train_val_test_split_function = function

    @property
    def compute_metrics_function(self) -> Callable:
        """The user can define a function that returns metrics from
        the predicted values and real data.

        The function should accept 1 or more arguments: the predicted targets.

          * The predicted targets are given automatically by AllOnIAModel when
            evaluating.
          * If the model is supervised (real targets are known), they are given
            as second argument.
          * If 'x' or 'X' appear in the possible arguments, then the predictive
            variables are passed to the function. It can be any positional
            argument.
          * If it is the first or second argument and the model is supervised,
            the other argument is the real targets, and predicted targets are
            not passed along.
          * Else, the first argument is the predicted targets (and if
            supervised the second is the real targets), and the predictive
            variables are passed as 'X'

        Any other argument must be passed as :ref:`custom_keyword` when
        learning.

        It should return a dictionary of metrics.

        To have your metrics displayed correctly on the plateform, please use
        the following keys in the returned dictionary:

         * For classification:
            - 'auc', 'recall', 'accuracy', 'f-measure', 'precision'
         * For regression:
            - 'mae', 'mse', 'rmse', 'r2'

        Using other keys will not fail the pipeline, but your metric will only
        be visible from the model ID Card, or from a notebook.

        Those keys are not mandatory, you can have a metric function only
        returning some or none of them without problem.
        """
        return self._compute_metrics_function

    @compute_metrics_function.setter
    @_limit_arguments(min_args=1)
    @typechecked
    def compute_metrics_function(self, function: Callable):
        args = list(inspect.signature(function).parameters.keys())
        if "X" in args and "x" in args:
            both_x_and_upper_x()
        self._compute_metrics_function = function

    @property
    def postprocess_function(self) -> Callable:
        """The user can define a post-processing function that takes at least 1
        argument: the predictions of the model.
        """
        return self._postprocess_function

    @postprocess_function.setter
    @_limit_arguments(min_args=1)
    @typechecked
    def postprocess_function(self, function: Callable):
        self._postprocess_function = function

    @property
    @getattr_safe_property
    def feature_engineering_summary(self) -> pd.DataFrame:
        return copy(self.feature_engineering_execs.summary)

    @property
    @getattr_safe_property
    def splits_summary(self) -> pd.DataFrame:
        return copy(self.split_execs.summary)

    @property
    @getattr_safe_property
    def learnings_summary(self) -> pd.DataFrame:
        return copy(self.learn_execs.summary)

    @property
    @getattr_safe_property
    def trainings_summary(self) -> pd.DataFrame:
        return copy(self.train_execs.summary)

    @property
    @getattr_safe_property
    def validations_summary(self) -> pd.DataFrame:
        return copy(self.validate_execs.summary)

    @property
    @getattr_safe_property
    def tests_summary(self) -> pd.DataFrame:
        return copy(self.test_execs.summary)

    @property
    @getattr_safe_property
    def applies_summary(self) -> pd.DataFrame:
        return copy(self.apply_execs.summary)

    @property
    @getattr_safe_property
    def predicts_summary(self) -> pd.DataFrame:
        return copy(self.predict_execs.summary)

    @property
    @getattr_safe_property
    def postprocesses_summary(self) -> pd.DataFrame:
        return copy(self.postprocess_execs.summary)

    # Public learning pipeline methods

    def health_check(
        self,
        force: bool = False,
        reshape_x: tuple[int, ...] | None = None,
        reshape_y: tuple[int, ...] | None = None,
        **kwargs,
    ) -> bool:
        """Will check that the full learning and prediction pipelines manage to
        run twithout errors.

        Will only run if :

          * the method never ran before.
          * any attribute impacting any of those pipelines was modified since
            last time this method ran.
          * :inlinepython:`force = True`. This can be useful, for
            example, if the data pointed to by :obj:`raw_set` was modified.
            Indeed, the model itself would not know it, but the
            user would still be able to rerun the check.
          * the last time it ran, this method returned False.

        Args:
            reshape_x: see :obj:`train`
            reshape_y: see :obj:`train`
            kwargs:
                >>> {
                >>>    # Kwargs to pass to self.model or self.model_class
                >>>    "model_kwargs": {...},
                >>>    # Kwargs to pass to feature_engineering_function
                >>>    "feature_engineering_kwargs": {...},
                >>>    # Kwargs to pass to train_val_test_split_function
                >>>    "train_val_test_split_kwargs": {...},
                >>>    # Kwargs to pass to self.model.fit
                >>>    "fit_kwargs": {...},
                >>>    # Kwargs to pass to self.model.predict when producing
                >>>    # predictions from test or validation set for metrics
                >>>    # evaluation.
                >>>    "predict_for_metrics_kwargs": {...},
                >>>    # Kwargs to pass to compute_metrics_function
                >>>    "metrics_kwargs": {...},
                >>>    # Kwargs to pass to self.model.predict when producing
                >>>    # predictions from observed data
                >>>    "predict_kwargs": {...},
                >>>    # Kwargs to pass to the postprocess_function
                >>>    "postprocess_kwargs": {...},
                >>> }
            force: If :inlinepython:`True`, the check will run the pipelines
                even though no important attributes was changed.

        Warns:
            :If the check started and failed or if the
            :obj:`health_check_set` attribute was not set.
        """
        _check_kwargs(kwargs, (), self._kwargs_dispatch_dict["health_check"])
        if self._rerun_health_check is True or force is True:
            if self._health_check_set._method == "empty":
                logger.warning(
                    f"Can not check AllOnIAModel '{self.name}' health as the "
                    "attribute 'health_check_set' is not defined."
                )
                self._healthy = False
            else:
                try:
                    obj = AllOnIAModel(
                        "health_check", read_only=True, do_not_log_open=True
                    )
                    obj.set_variables(
                        self.predictive_variables, self.target_variables
                    )
                    for attr in self.triggers_health_check:
                        if attr not in (
                            "raw_set",
                            "predictive_variables",
                            "target_variables",
                        ):
                            # Important to copy ! If we set 'obj' model to point
                            # to the same memory address as self, then train
                            # obj, self.model will also be modified.
                            value = getattr(self, attr)
                            if value is None:
                                continue
                            setattr(obj, attr, deepcopy(value))
                    obj.raw_set = self.health_check_set
                    obj.observations_set = (
                        self.health_check_observations_set
                        if self._health_check_observations_set._method
                        != "empty"
                        else self.health_check_set
                    )
                    obj.learn(
                        reshape_x=reshape_x,
                        reshape_y=reshape_y,
                        **{
                            key: copy(kwargs.get(key, {}))
                            for key in self._kwargs_dispatch_dict["learn"]
                        },
                    )
                    if obj.target_variables:
                        obj.apply(
                            reshape_x=reshape_x,
                            **{
                                key: copy(kwargs.get(key, {}))
                                for key in self._kwargs_dispatch_dict["apply"]
                            },
                        )
                    self._healthy = True
                except Exception as error:
                    logger.warning(
                        f"Health check failed for AllOnIAModel '{self.name}'"
                        f" with error {error}."
                    )
                    self._healthy = False

        self._rerun_health_check = not self._healthy
        return self._healthy

    @ReadyDecorator.ready(
        needed_attributes=(
            "fit_function_name",
            "raw_set | derived_set | train_set",
            "_model | _model_class",
            "predictive_variables",
        )
    )
    @_record_execution(to_attribute="learn_execs", record_results=True)
    def learn(
        self,
        reshape_x: tuple[int, ...] | None = None,
        reshape_y: tuple[int, ...] | None = None,
        **kwargs,
    ):
        """Runs the full pipeline *feature engineering-split
        -train-validate-test*,
        sends a summary to validators and returns the validation and test
        metrics.

        Needs one of :obj:`raw_set`,
        :obj:`derived_set`
        or :obj:`train_set` to be defined. If
        :obj:`raw_set` is defined, the entiere pipeline runs
        (feature engineering, split, train, evaluate), if not but
        :obj:`derived_set` is defined, then feature engineering is
        skipped, and if only :obj:`train_set` is defined, both
        feature engineering and split are skipped.

        Args:
            reshape_x: see :obj:`train`
            reshape_y: see :obj:`train`
            kwargs:
                >>> {
                >>>    # Kwargs to pass to self.model or self.model_class
                >>>    "model_kwargs": {...},
                >>>    # Kwargs to pass to feature_engineering_function
                >>>    "feature_engineering_kwargs": {...},
                >>>    # Kwargs to pass to train_val_test_split_function
                >>>    "train_val_test_split_kwargs": {...},
                >>>    # Kwargs to pass to self.model.fit
                >>>    "fit_kwargs": {...},
                >>>    # Kwargs to pass to self.model.predict when producing
                >>>    # predictions from test or validation set for metrics
                >>>    # evaluation.
                >>>    "predict_for_metrics_kwargs": {...},
                >>>    # Kwargs to pass to compute_metrics_function
                >>>    "metrics_kwargs": {...},
                >>> }


        Returns:
            Validation and test metrics

        See Also:
            :obj:`apply`
        """
        _check_kwargs(kwargs, (), self._kwargs_dispatch_dict["learn"])
        if self.model_class is not None:
            # Recreate 'model' each time if 'model_class' is not None, to
            # allow for hyperparameter optimisation
            self.model = self.model_class(
                **copy(kwargs.get("model_kwargs", {}))
            )
        if self.raw_set is not None:
            self.feature_engineering(
                "raw",
                __skip_description_update=True,
                **copy(kwargs.get("feature_engineering_kwargs", {})),
            )
        if self.derived_set is not None:
            self.train_val_test_split(
                __skip_description_update=True,
                **copy(kwargs.get("train_val_test_split_kwargs", {})),
            )
        self.train(
            reshape_x=reshape_x,
            reshape_y=reshape_y,
            __skip_description_update=True,
            **copy(kwargs.get("fit_kwargs", {})),
        )
        evaluate_kwargs = {
            key: copy(kwargs.get(key, {}))
            for key in self._kwargs_dispatch_dict["evaluate"]
        }

        validation_metrics = self.validate(
            reshape_x=reshape_x,
            __skip_description_update=True,
            **evaluate_kwargs,
        )
        test_metrics = self.test(
            reshape_x=reshape_x,
            __skip_description_update=True,
            **evaluate_kwargs,
        )

        self._send_summary()
        return {
            "results": (validation_metrics, test_metrics),
            "model": self.model_name,
            "dataset_revision": {
                "raw_set": (
                    self._raw_set.pointer_str,
                    self._raw_set._revision,
                )
            },
        }

    @_record_execution(
        to_attribute="feature_engineering_execs", record_results=False
    )
    @convert_self_kwarg
    @typechecked
    def feature_engineering(self, raw_or_observed: str, **kwargs):
        """Pre-processes the raw dataset using
        :obj:`feature_engineering_function`

        Args:
            raw_or_observed: Should the function run or the *raw* dataset
                (for learning) or the *observed* dataset (for predictions) ?
            kwargs: keyword arguments to pass to
                :obj:`feature_engineering_function`.

        Returns:
            The derived data
        """
        if raw_or_observed == FeatEngSetToUse.raw.value:
            data = self.raw_set
            dataset_revision = {
                "raw_set": (self._raw_set.pointer_str, self._raw_set._revision)
            }
            if data is None:
                raise NotReadyError("feature engineering", ["raw_set"])
        elif raw_or_observed == FeatEngSetToUse.observed.value:
            data = self.observations_set
            dataset_revision = {
                "observations_set": (
                    self._observations_set.pointer_str,
                    self._observations_set._revision,
                )
            }
            if data is None:
                raise NotReadyError("feature engineering", ["observations_set"])
            self._input_sample = get_data_sample(data)
        else:
            raise raw_or_observed_err(raw_or_observed)

        result = self.feature_engineering_function(data, **kwargs)
        if result is None:
            raise feat_eng_return_err()
        if raw_or_observed == "raw":
            self.derived_set = result
        else:
            self.derived_observations_set = result
        return {
            "results": copy(result),
            "model": self.model_name,
            "dataset_revision": dataset_revision,
        }

    @_record_execution(to_attribute="split_execs", record_results=False)
    @ReadyDecorator.ready(needed_attributes=("derived_set",))
    @convert_self_kwarg
    def train_val_test_split(self, **kwargs):
        """Splits the derived data in train-validation-test sets.

        Args:
            kwargs: keyword arguments to pass to
                :obj:`train_val_test_split_function`

        Returns:
            train, validation and test sets
        """
        train_size = 1.0 - self._test_set_size
        validation_size = self._validation_set_size / train_size

        if self._test_set_size > 0:
            train, test = self.train_val_test_split_function(
                self.derived_set,
                test_size=self._test_set_size,
                random_state=self._random_state,
                **kwargs,
            )
        else:
            train = self.derived_set
            test = None

        if validation_size > 0:
            train, validation = self.train_val_test_split_function(
                train,
                test_size=validation_size,
                random_state=self._random_state,
                **kwargs,
            )
        else:
            validation = None

        self.train_set = train
        self.validation_set = validation
        self.test_set = test
        return {
            "results": (copy(train), copy(validation), copy(test)),
            "model": self.model_name,
            "dataset_revision": {
                "derived_set": (
                    self._derived_set.pointer_str,
                    self._derived_set._revision,
                )
            },
        }

    @ReadyDecorator.ready(
        needed_attributes=(
            "fit_function_name",
            "train_set",
            "_model",
            "predictive_variables",
        )
    )
    @_record_execution(to_attribute="train_execs", record_results=False)
    @convert_self_kwarg
    def train(
        self,
        reshape_x: tuple[int, ...] | None = None,
        reshape_y: tuple[int, ...] | None = None,
        **kwargs,
    ):
        """Trains the model on the train set.

        Args:
            reshape_x: If the X data needs to be reshapen, yuocan pass its new
                shape here. For instance, sklearn.LinearRegression needs 2-D
                arrays, even if there is only on feature in X. And since by
                default AllOnIAModel will squeeze any 1-featured array into a
                1-D array, you must then give 'reshape_x=(-1, 1)' to the
                train method.
            reshape_y: same as reshape_x but for y
            kwargs: keyword arguments to pass to the model's fit function.
                Remember that X and y are passed automatically, do not specify
                them here.
        """

        y = None
        x = get_variable(
            self.train_set, self._predictive_variables, "predictive"
        )
        # Just to trigger self.description update
        self._predictive_variables = self._predictive_variables
        if self._target_variables is not None:
            y = get_variable(self.train_set, self._target_variables, "target")
            # Just to trigger self.description update
            self._target_variables = self._target_variables
            # When y is a 1-D array and contains integers, booleans or strings,
            # we assume we are in a classification problem and save the
            # unique values of y as classes.
            if (
                hasattr(y, "shape")
                and len(y.shape) == 1
                and self.target_variables.types[0] in (int, bool, str)
            ):
                classes = np.unique(y)
                classes.sort()
                self.classes = classes
                self._target_variables.data["classes"] = (self.classes,)

        x = reshape(x, reshape_x)
        y = reshape(y, reshape_y)

        fit = getattr(self._model, self.fit_function_name)
        fit(x, y, **kwargs) if y is not None else fit(x, **kwargs)
        return {
            "results": None,
            "model": self.model_name,
            "dataset_revision": {
                "train_set": (
                    self._train_set.pointer_str,
                    self._train_set._revision,
                )
            },
        }

    @ReadyDecorator.ready(
        needed_attributes=(
            "predict_function_name",
            "_model",
            "predictive_variables",
        )
    )
    @_record_execution(to_attribute="validate_execs", record_results=True)
    @convert_self_kwarg
    def validate(self, reshape_x: tuple[int, ...] | None = None, **kwargs):
        """Validates the model by making predictions from the validation
        dataset's predictive variables, and computes metrics using the
        :obj:`compute_metrics_function` and the validation dataset's target
        variables. Both metrics and predictions are recorded in the AllOnIAModel
        instance.

        Args:
            reshape_x: see :obj:`predict`
            kwargs:
                >>> {
                >>>    # Kwargs to pass to self.model.predict when producing
                >>>    # predictions from test or validation set for metrics
                >>>    # evaluation.
                >>>    "predict_for_metrics_kwargs": {...},
                >>>    # Kwargs to pass the compute_metrics_function
                >>>    "metrics_kwargs": {...},
                >>> }

        Returns:
            The metrics returned by :obj:`compute_metrics_function`.
        """
        return {
            "results": (
                copy(self.evaluate("validation", reshape_x=reshape_x, **kwargs))
            ),
            "model": self.model_name,
            "dataset_revision": {
                "validation_set": (
                    self._validation_set.pointer_str,
                    self._validation_set._revision,
                )
            },
        }

    @ReadyDecorator.ready(
        needed_attributes=(
            "predict_function_name",
            "_model",
            "predictive_variables",
        )
    )
    @_record_execution(to_attribute="test_execs", record_results=True)
    @convert_self_kwarg
    def test(self, reshape_x: tuple[int, ...] | None = None, **kwargs):
        """Tests the model by making predictions from the test
        dataset's predictive variables, and computes metrics using the
        :obj:`compute_metrics_function` and the test dataset's target variables.
        Both metrics and predictions are recorded in the AllOnIAModel instance.

        Args:
            reshape_x: see :obj:`predict`
            kwargs:
                >>> {
                >>>    # Kwargs to pass to self.model.predict when producing
                >>>    # predictions from test or validation set for metrics
                >>>    # evaluation.
                >>>    "predict_for_metrics_kwargs": {...},
                >>>    # Kwargs to pass the compute_metrics_function
                >>>    "metrics_kwargs": {...},
                >>> }

        Returns:
            The metrics returned by :obj:`compute_metrics_function`.
        """
        return {
            "results": (
                copy(self.evaluate("test", reshape_x=reshape_x, **kwargs))
            ),
            "model": self.model_name,
            "dataset_revision": {
                "test_set": (
                    self._test_set.pointer_str,
                    self._test_set._revision,
                )
            },
        }

    @ReadyDecorator.ready(
        needed_attributes=(
            "predict_function_name",
            "_model",
            "predictive_variables",
        )
    )
    def evaluate(  # noqa: PLR0912
        self,
        test_or_validation: str,
        reshape_x: tuple[int, ...] | None = None,
        **kwargs,
    ) -> dict:
        """:obj:`model` must have been fitted before.

        Will call :obj:`model`'s *predict* method on the
        :obj:`predictive_variables` variables in the validation or test set
        (depending on the value of *test_or_validation*), and compare the
        predicted values to the :obj:`target_variables` variables on the same
        set using :obj:`compute_metrics_function`.

        Predictions are saved in the current AllOnIAModel instance.

        Args:
            test_or_validation: "validation" or "test"
            reshape_x: see :obj:`predict`
            kwargs:
                >>> {
                >>>    # Kwargs to pass to self.model.predict when producing
                >>>    # predictions from test or validation set for metrics
                >>>    # evaluation.
                >>>    "predict_for_metrics_kwargs": {...},
                >>>    # Kwargs to pass the compute_metrics_function
                >>>    "metrics_kwargs": {...},
                >>> }

                kwargs to pass to :obj:`model.predict` and
                :obj:`model.compute_metrics_function`

        Returns:
            The result of :obj:`compute_metrics_function`, which is supposed to
                be a dictionary of metrics.
        """
        _check_kwargs(kwargs, (), self._kwargs_dispatch_dict["evaluate"])

        if test_or_validation == "validation":
            data = self.validation_set
        elif test_or_validation == "test":
            data = self.test_set
        else:
            raise invalid_test_validate_value_err(test_or_validation)
        if (
            (isinstance(data, np.ndarray) and data.shape[0] == 0)
            or (isinstance(data, pd.DataFrame) and data.empty)
            or data is None
        ):
            logger.warning(
                f"Skipping {test_or_validation} as the corresponding set is "
                f"empty"
            )
            return {}

        y = None
        x = get_variable(data, self._predictive_variables, "predictive")
        if self._target_variables is not None:
            y = get_variable(data, self._target_variables, "target")

        x = reshape(x, reshape_x)
        # Do not call `predict`, not to record this prediction run in
        # the list of execution metadata, since we are only interested in
        # predictions on observations in those metadata.
        predictions = getattr(self._model, self.predict_function_name)(
            x, **copy(kwargs.get("predict_for_metrics_kwargs", {}))
        )
        metrics_kwargs = copy(kwargs.get("metrics_kwargs", {}))
        expected_args = list(
            inspect.signature(self._compute_metrics_function).parameters
        )
        if (
            "x" not in expected_args
            and "X" not in expected_args
            or ("x" in metrics_kwargs or "X" in metrics_kwargs)
        ):
            metrics_args = (predictions, y) if y is not None else (predictions,)
        else:
            x_name = "x" if "x" in expected_args else "X"
            # With targets
            if y is not None:
                if expected_args.index(x_name) == 0:
                    metrics_args = (x, y)
                elif expected_args.index(x_name) == 1:
                    metrics_args = (y, x)
                else:
                    metrics_args = (predictions, y)
                    metrics_kwargs[x_name] = x
            # Without targets (for example, clustering)
            elif expected_args.index(x_name) == 0:
                metrics_args = (x,)
            else:
                metrics_args = (predictions,)
                metrics_kwargs[x_name] = x

        metrics = self._compute_metrics_function(
            *metrics_args, **metrics_kwargs
        )
        self._set_predictions(test_or_validation, predictions)
        return metrics

    # Public prediction pipeline methods

    @ReadyDecorator.ready(
        needed_attributes=(
            "predict_function_name",
            "observations_set | derived_observations_set",
            "_model",
            "predictive_variables",
        )
    )
    @_record_execution(to_attribute="apply_execs", record_results=False)
    def apply(self, reshape_x: tuple[int, ...] | None = None, **kwargs):
        """Runs the full prediction pipeline *feature
        engineering-prediction-postprocessing* and returns the postprocessed
        predictions given by :obj:`postprocess_function`.

        Needs one of :obj:`observations_set`
        or :obj:`derived_observations_set` to be defined. If
        :obj:`observations_set` is defined, the entire pipeline
        runs (feature engineering, predict), if not, then feature engineering is
        skipped.

        Args:
            reshape_x: see :obj:`predict`
            kwargs:
                >>> {
                >>>    # Kwargs to pass to feature_engineering_function
                >>>    "feature_engineering_kwargs": {...},
                >>>    # Kwargs to pass to self.model.predict when producing
                >>>    # predictions from observed data
                >>>    "predict_kwargs": {...},
                >>>    # Kwargs to pass to the postprocess_function
                >>>    "postprocess_kwargs": {...},
                >>> }

        Returns:
            Postprocessed predictions

        See Also:
            :obj:`learn`
        """
        _check_kwargs(kwargs, (), self._kwargs_dispatch_dict["apply"])
        if self.observations_set is not None:
            self.feature_engineering(
                "observed",
                __skip_description_update=True,
                **copy(kwargs.get("feature_engineering_kwargs", {})),
            )
        self.predict(
            reshape_x=reshape_x,
            __skip_description_update=True,
            **copy(kwargs.get("predict_kwargs", {})),
        )
        results = self.postprocess(
            __skip_description_update=True,
            **copy(kwargs.get("postprocess_kwargs", {})),
        )
        self._output_sample = get_data_sample(results)
        return {
            "results": results,
            "model": self.model_name,
            "dataset_revision": {
                "observations_set": (
                    self._observations_set.pointer_str,
                    self._observations_set._revision,
                )
            },
        }

    @ReadyDecorator.ready(
        needed_attributes=(
            "derived_observations_set",
            "_model",
            "predictive_variables",
        )
    )
    @_record_execution(to_attribute="predict_execs", record_results=False)
    @convert_self_kwarg
    def predict(self, reshape_x: tuple[int, ...] | None = None, **kwargs):
        """Predicts the target variables from the derived observations
        dataset's predictive variables.

        Args:
            reshape_x: same idea as :obj:`train`
            kwargs: Keyword arguments to pass to the model's predict function.
                Remember that X is passed automatically, do not specify it here.

        Returns:
            The predicted values.
        """
        x = get_variable(
            self.derived_observations_set,
            self._predictive_variables,
            "predictive",
        )
        x = reshape(x, reshape_x)
        predictions = getattr(self._model, self.predict_function_name)(
            x, **kwargs
        )
        self._set_predictions("observations", predictions)
        return {
            "results": copy(predictions),
            "model": self.model_name,
            "dataset_revision": {
                "derived_observations_set": (
                    self._derived_observations_set.pointer_str,
                    self._derived_observations_set._revision,
                )
            },
        }

    @_record_execution(to_attribute="postprocess_execs", record_results=False)
    @convert_self_kwarg
    def postprocess(self, **kwargs):
        """Post-processes the predictions made from the observations dataset,
        using :obj:`postprocess_function`, records the results in the
        AllOnIAModel instance and returns them.

        Args:
            kwargs: Keyword arguments to pass to :obj:`postprocess_function`.
                Remember that predictions are passed automatically, do not
                specify them here.

        Returns:
            The post-processed predictions.
        """
        predictions = self.get_predictions("observations")
        if predictions is None:
            raise NotReadyError("postprocess", ["predictions[observations]"])
        results = self.postprocess_function(predictions, **kwargs)
        self.postprocessed_predictions_set = results
        return {
            "results": copy(results),
            "model": self.model_name,
            "dataset_revision": {},
        }

    # Other public methods

    def get_predictions(
        self, set_name: str
    ) -> np.ndarray | pd.DataFrame | pd.Series | None:
        """Returns the predictions that have already been computed for the given
        set.

        Args:
            set_name: Can be any name specified in
                :obj:`_valid_set_names`.
        """
        return self._predictions[set_name]()

    def compare_requirements(self, modules: list[_Requirement]):
        """Checks that the requirements specified in *modules* and
        the currently installed packages match, raising
        :obj:`ModuleNotFoundError` if any package is missing. Will only warn
        if versions are different."""
        if (installed_python_version := platform.python_version()) != (
            req_python_version := self._requirements[
                self._requirements.index("Python")
            ].version
        ):
            # Do not raise an error for a difference in Python version, just
            # warn.
            logger.warning(
                f"Previous execution of model {self.name} required "
                f"Python {req_python_version}, but Python "
                f"{installed_python_version} is installed."
            )
        for req in self._requirements:
            if req == "Python":
                continue
            if req not in modules:
                try:
                    # The requirements might be installed, but not imported yet,
                    # so not present in the current sys.modules. Try to
                    # import it, and fetch its version.
                    __import__(req.name)
                    module = _Requirement(
                        req.name, sys.modules[req.name].__version__
                    )
                except (ModuleNotFoundError, AttributeError) as error:
                    raise invalid_req_err(self.name, req.name) from error
            else:
                module = modules[modules.index(req)]
            if module.version != req.version:
                logger.warning(
                    f"Previous execution of model {self.name} required "
                    f"module {req.name} with version {req.version}, but "
                    f"version {module.version} is installed."
                )

    def set_requirements(self):
        """The user can decide to update the required packages to the
        installed one before saving a new version of the model by calling this
        method."""
        self._requirements = self._get_imported_packages(True)

    def save(self):
        """Saves the AllOnIAModel instance.

        Will pickle the object in a binary file in
        ':obj:`root`/model/:obj:`name`/model.aleiamodel' and
        its :obj:`description` in a json file in
        ':obj:`root`/model/:obj:`name`/description.json'.

        The saved model will not retain any raw, pre-processed, predicted,
        observed nor post-processed data, as those can be heavy. Except for
        :obj:`raw_set`, :obj:`observations_set`, :obj:`health_check_set`
        and :obj:`health_check_observations_set`:
        if they were specified as :obj:`str` or collections of :obj:`str`, those
        are saved.

        Raises:
            :obj:`utils.ReadOnlyError`: If the model is read-only
        """

        if self.read_only:
            raise ReadOnlyError("Can not save : model is read-only")

        results = {"binary_save": self.binary_path.write(self)}
        versions = self.list_versions(self.name)
        # Could also read it from the last line of 'versions'...
        if not results["binary_save"].success:
            raise OSError(f"Could not write {self}")
        self._version_id = results["binary_save"].version_id
        self._update_execution_lists_versions()
        results["description_save"] = self.version_named_description_path.write(
            self._version_id,
            self.description,
            copy_to_latest=True,
            versions=versions,
        )

        if self.model is not None:
            results["seldon_save"] = self.version_named_seldon_path.write(
                self._version_id,
                self.model,
                copy_to_latest=True,
                versions=versions,
            )
        return results

    def get_requirements(self) -> str:
        """Return a :obj:`str` that can be written to a requirements.txt file,
        that can be used to install packages with pip.
        """
        return "\n".join([str(r) for r in self._requirements if r != "Python"])

    def close(self):
        """Logs the closing of the model, releases the lock and sets the model
        to 'read_only'."""
        self._log_closing(None, None)
        errors = self._release_lock(None, None)
        if errors:
            logger.info(
                f"Failed to release lock for one AllOnIAModel: {errors}.",
            )
        else:
            self._read_only = True
            logger.info(
                f"Closed model {self.name}. It is now available for other users"
                f" in edition mode.",
            )
