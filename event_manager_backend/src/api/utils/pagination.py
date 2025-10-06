from __future__ import annotations

from typing import Tuple


# PUBLIC_INTERFACE
def parse_pagination(limit: int | None = None, offset: int | None = None, default_limit: int = 20, max_limit: int = 100) -> Tuple[int, int]:
    """Parse pagination parameters, clamp values, and return (limit, offset)."""
    if limit is None or limit <= 0:
        limit = default_limit
    if limit > max_limit:
        limit = max_limit
    if offset is None or offset < 0:
        offset = 0
    return limit, offset
