"""End-to-end molecular-data entry point for the hybrid indexer."""

from pathlib import Path
from os import PathLike

import che_inter
import hybrid_indexer


def che_file_to_knot_name(
    che_file_path: str,
    *,
    java_path: str | PathLike[str] | None = None,
    sage_path: str | PathLike[str] | None = None,
    projection_timeout: float = 120.0,
    khovanov_timeout: float = 120.0,
    homfly_timeout: float = 120.0,
    max_heap: str = "16g",
) -> list[str]:
    path = Path(che_file_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    pd_code = che_inter.che_data_to_pd_code(str(path), timeout=projection_timeout)
    return hybrid_indexer.hybrid_indexer(
        pd_code,
        java_path=java_path,
        sage_path=sage_path,
        khovanov_timeout=khovanov_timeout,
        homfly_timeout=homfly_timeout,
        max_heap=max_heap,
    )
