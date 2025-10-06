from __future__ import annotations

from datetime import datetime
from fastapi import HTTPException, status


# PUBLIC_INTERFACE
def ensure_valid_time_range(start: datetime, end: datetime | None) -> None:
    """Validate that end time is not before start time."""
    if end is not None and end < start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end_time cannot be before start_time")
