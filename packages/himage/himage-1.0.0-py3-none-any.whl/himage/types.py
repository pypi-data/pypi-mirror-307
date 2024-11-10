import numpy.typing as npt
from typing import Any, Literal, Union

Image = npt.NDArray[Any]
Real = Union[int, float]
UpperLimit = Literal[255, 1]