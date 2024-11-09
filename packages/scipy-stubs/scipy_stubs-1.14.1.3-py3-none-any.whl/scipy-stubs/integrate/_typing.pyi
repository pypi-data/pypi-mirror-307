# type-check-only typing utilities for internal usage
from typing import Any, Literal, TypeAlias, TypedDict, type_check_only
from typing_extensions import NotRequired

import numpy as np
import numpy.typing as npt
import optype.numpy as onpt
from numpy._typing import _ArrayLikeFloat_co

__all__ = "ODEInfoDict", "QuadInfoDict", "QuadOpts", "QuadWeights"

_IntLike: TypeAlias = int | np.integer[Any]
_FloatLike: TypeAlias = float | np.floating[Any]

QuadWeights: TypeAlias = Literal["cos", "sin", "alg", "alg-loga", "alg-logb", "alg-log", "cauchy"]

@type_check_only
class QuadOpts(TypedDict, total=False):
    epsabs: _FloatLike
    epsrel: _FloatLike
    limit: _IntLike
    points: _ArrayLikeFloat_co
    weight: QuadWeights
    wvar: _FloatLike | tuple[_FloatLike, _FloatLike]
    wopts: tuple[_IntLike, npt.NDArray[np.float32 | np.float64]]

@type_check_only
class QuadInfoDict(TypedDict):
    neval: int
    last: int
    alist: onpt.Array[tuple[int], np.float64]
    blist: onpt.Array[tuple[int], np.float64]
    rlist: onpt.Array[tuple[int], np.float64]
    elist: onpt.Array[tuple[int], np.float64]
    iord: onpt.Array[tuple[int], np.int_]

    # if `points` is provided
    pts: NotRequired[onpt.Array[tuple[int], np.float64]]
    level: NotRequired[onpt.Array[tuple[int], np.int_]]
    ndin: NotRequired[onpt.Array[tuple[int], np.int_]]

    # finite integration limits
    momcom: NotRequired[float | np.float64]
    nnlog: NotRequired[onpt.Array[tuple[int], np.int_]]
    chebmo: NotRequired[onpt.Array[tuple[Literal[25], int], np.int_]]

    # single infitite integration limit and numerical error
    lst: NotRequired[int]
    rslst: NotRequired[onpt.Array[tuple[int], np.float64]]
    erlst: NotRequired[onpt.Array[tuple[int], np.float64]]
    ierlst: NotRequired[onpt.Array[tuple[int], np.float64]]

@type_check_only
class ODEInfoDict(TypedDict):
    hu: onpt.Array[tuple[int], np.float64]
    tcur: onpt.Array[tuple[int], np.float64]
    tolsf: onpt.Array[tuple[int], np.float64]
    tsw: float
    nst: int
    nfe: int
    nje: int
    nqu: onpt.Array[tuple[int], np.int_]
    imxer: int
    lenrw: int
    leniw: int
    mused: onpt.Array[tuple[int], np.int_]
