from typing import TypeAlias

import jax.typing as jxt
import numpy.typing as npt

ArrayLike: TypeAlias = npt.ArrayLike | jxt.ArrayLike
