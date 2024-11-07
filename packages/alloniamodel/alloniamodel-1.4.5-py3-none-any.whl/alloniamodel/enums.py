from enum import Enum, unique


class ExtendedEnum(Enum):
    """
    An extended version of the Enum class that provides additional
    functionality.

    Methods:
        :list(cls, exclude=None): Returns a list of enum values, excluding any
                                  values specified in the `exclude` list.
    """

    @classmethod
    def list(cls, exclude=None):
        """
        Return a list of enum values, optionally excluding specified values.

        Args:
            exclude (list, optional): A list of enum values to exclude. Defaults
                                      to None.

        Returns:
            list: A list of enum values.
        """
        if exclude is None:
            exclude = []
        return (
            [enumeration.value for enumeration in cls]
            if len(exclude) == 0
            else [
                enumeration.value
                for enumeration in cls
                if enumeration.value not in exclude
            ]
        )

    def __str__(self):
        """
        Return the string representation of the enum value.

        Returns:
            :str: The string representation of the enum value.
        """
        return self.value


@unique
class FeatEngSetToUse(ExtendedEnum):
    raw = "raw"
    observed = "observed"


@unique
class TestOrValidationSet(ExtendedEnum):
    test = "test"
    validation = "validate"
