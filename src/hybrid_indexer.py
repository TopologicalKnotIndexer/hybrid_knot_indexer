"""Intersect Khovanov and HOMFLY-PT catalog candidates."""

from os import PathLike

import hom_inter
import kho_inter


def merge_name_list(namelist_kho: list[str], namelist_hom: list[str]) -> list[str]:
    """Return the sorted set intersection of both invariant candidate lists."""

    if not isinstance(namelist_kho, list) or not isinstance(namelist_hom, list):
        raise TypeError("candidate collections must be lists")
    return sorted(set(namelist_kho) & set(namelist_hom))


def hybrid_indexer(
    pd_code: list[list[int]],
    *,
    java_path: str | PathLike[str] | None = None,
    sage_path: str | PathLike[str] | None = None,
    khovanov_timeout: float = 120.0,
    homfly_timeout: float = 120.0,
    max_heap: str = "16g",
) -> list[str]:
    """Return candidates satisfying the available invariant catalog filters.

    A zero- or one-element Khovanov result is already definitive within the
    finite catalog, so HOMFLY-PT is only evaluated for ambiguous Khovanov rows.
    Backend failures are explicit exceptions; an empty list means no match.
    """

    khovanov_names = sorted(
        set(
            kho_inter.to_knotname(
                pd_code,
                java_path=java_path,
                timeout=khovanov_timeout,
                max_heap=max_heap,
            )
        )
    )
    if len(khovanov_names) <= 1:
        return khovanov_names
    homfly_names = hom_inter.to_knotname(
        pd_code, sage_path=sage_path, timeout=homfly_timeout
    )
    return merge_name_list(khovanov_names, homfly_names)
