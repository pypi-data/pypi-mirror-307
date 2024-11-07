from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from allonias3 import S3Path

from .enums import FeatEngSetToUse, TestOrValidationSet


class ReadOnlyError(Exception):
    """Custom error raised by
    :obj:`~aleiamodel.model.AleiaModel` when trying to save a read-only model,
    or trying to open a model not in read-only but when the lockfile exists."""


class VersionNotFoundError(ValueError):
    """Custom error raised by
    :obj:`~aleiamodel.model.AleiaModel` when trying to open a specific version
    or revision that does not exist on S3."""

    def __init__(
        self,
        name: str,
        version: str = "",
        revision: None | int = None,
        *args,
    ):
        super().__init__(args)
        self.name = name
        self.version = version
        self.revision = revision

    def __str__(self):
        if self.revision:
            return f"Model {self.name} has no revision number {self.revision}."
        return f"Model {self.name} has no version UUID {self.version}."


class NotReadyError(Exception):
    """Custom error raised by the
    :obj:`~aleiamodel.decorator.ReadyDecorator.ready` decorator to inform that
    a function of the learning or prediction pipeline is not ready to run
    yet because some user-defined information is missing."""

    def __init__(self, what_for: str, missing_attrs: list[str], *args):
        super().__init__(args)
        self.what_for = what_for
        self.missing_attrs = missing_attrs

    def __str__(self):
        s = "\n * ".join(self.missing_attrs)
        return (
            f"Not ready to start {self.what_for}. Please provide one of the"
            f" following attribute(s): \n * {s}"
        )


def invalid_revision_err(n_versions: None | int = None):
    if n_versions is None:
        return ValueError("Revision number starts at 1, not 0.")
    return ValueError(f"Model only has {n_versions} revisions.")


def data_type_err(wrong_type: type):
    return TypeError(f"Invalid type {wrong_type} for element of data")


def fewer_revisions_than_data_err(revision: int | list | tuple, n_data: int):
    revisions = 1 if not isinstance(revision, (tuple, list)) else len(revision)
    raise ValueError(
        f"{n_data} file(s) was(were) provided to DataHandler but {revisions}"
        " revision(s) was(were) specified."
    )


def missing_loading_method_err(method: str):
    return NotImplementedError(
        f"Loading with '{method}' method is not implemented"
    )


def version_and_revision_err():
    return ValueError("Can not specify both version and revision")


def model_binary_not_fount_err(missing_file: S3Path):
    return FileNotFoundError(
        f"AllOnIAModel's file {missing_file} does not exists"
    )


def lockfile_exists_err(name: str, lockfile: S3Path):
    return ReadOnlyError(
        f"Model {name} is already open somewhere. You can open it "
        f"in read-only mode only. If you are sure that no other "
        f"process is using this model with the intention to modify "
        f"it, you can remove the file with "
        f"allonias3.S3Path('{lockfile}', persistent=False).rm()."
    )


def model_should_implement_err(expected: str):
    return AttributeError(
        f"The model object should implement the '{expected}' method. If another"
        " method should be used, set the AleiaModel's 'fit_function_name' or"
        " 'predict_function_name'  accordingly before setting the model."
    )


def invalid_test_validate_value_err(test_or_validation: str):
    return ValueError(
        f"Invalid value '{test_or_validation}' for test_or_validation"
        f" argument. Can be one of {TestOrValidationSet.list()}."
    )


def health_check_failed_err():
    return ValueError(
        "Can not set 'is_production' to True if 'health_check' fails."
    )


def set_size_err(set_name: str = ""):
    if set_name:
        return ValueError(f"{set_name} set size must be between 0 and 1")
    return ValueError(
        "The sum of the test and validation sizes must be inferior to 1"
    )


def raw_or_observed_err(raw_or_observed: str):
    return ValueError(
        f"Invalid value '{raw_or_observed}' for raw_or_observed. Can"
        f" be one of {FeatEngSetToUse.list()}."
    )


def feat_eng_return_err():
    return ValueError("Feature engineering function must not return None")


def invalid_req_err(name: str, req: str):
    return ModuleNotFoundError(
        f"Previous execution of model {name} required module {req}"
    )


def cannot_record_err(to_attribute: str, type_attribute: str):
    return TypeError(
        f"Can not record execution metadata in attribute "
        f"{to_attribute}. Needs to be a ExecutionList, is a "
        f"{type_attribute}"
    )


def invalid_limit_arg_err(which: str):
    if which == "one":
        return ValueError(
            "If 'number_of_args' is specified, neither 'min_args' nor"
            " 'max_args' can be used"
        )
    if which == "none":
        return ValueError(
            "At least one of 'number_of_args', 'min_args' or 'max_args'"
            " must be specified"
        )
    if which == "all":
        return ValueError("'min_args' can not be greater than 'max_args'")
    return None


def limit_arg_err(
    nargs: int,
    number_of_args: int | None = None,
    min_args: int | None = None,
    max_args: int | None = None,
):
    if number_of_args:
        return ValueError(
            f"This function must accept {number_of_args} and only "
            f"{number_of_args} argument. {nargs} were specified."
        )
    if min_args:
        return ValueError(
            f"This function must accept at least {min_args}"
            f" arguments. {nargs} were specified."
        )
    if max_args:
        return ValueError(
            f"This function must accept at most {max_args}"
            f" arguments. {nargs} were specified."
        )
    return None


def verion_not_updated_err():
    raise TimeoutError(
        "The model did not have versions after 10 secondes while it has a "
        "binary file. Most likely, the DB did not update correctly. Wait a bit "
        "and retry."
    )


def invalid_kwargs_err(error: str):
    raise ValueError(error)


def both_x_and_upper_x():
    raise ValueError(
        "compute_metrics_function can not accept both 'x' and 'X' as argument,"
        " as AleiaModel will not know which one is expected to be the "
        "predictive variables."
    )
