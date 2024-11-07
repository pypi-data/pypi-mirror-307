from .decorator import convert_self_kwarg
from .model import AllOnIAModel
from .utils import URL, SpecialDataFormat
from .variables import Variables

print(
    "You can check out alloniamodel's documentation here:\n"
    "https://aleia-team.gitlab.io/public/alloniamodel"
)

__all__ = [
    "AllOnIAModel",
    "Variables",
    "SpecialDataFormat",
    "URL",
    "convert_self_kwarg",
]
