from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Path, Query, status
from ..dependencies.auth import verify_firebase_token
from ..models.schemas import EventCreate, EventOut, EventUpdate, Paginated, CurrentUser
from ..utils.pagination import parse_pagination
from ..utils.validation import ensure_valid_time_range

router = APIRouter(prefix="/events", tags=["Events"])


# PUBLIC_INTERFACE
@router.get(
    "",
    summary="List events",
    response_model=Paginated[EventOut],
)
def list_events(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: CurrentUser = Depends(verify_firebase_token),
):
    """List events for the authenticated user."""
    l, o = parse_pagination(limit, offset)
    return Paginated[EventOut](items=[], limit=l, offset=o, total=0, next_offset=None)


# PUBLIC_INTERFACE
@router.post(
    "",
    summary="Create event",
    response_model=EventOut,
    status_code=status.HTTP_201_CREATED,
)
def create_event(payload: EventCreate, current_user: CurrentUser = Depends(verify_firebase_token)):
    """Create a new event for the authenticated user."""
    ensure_valid_time_range(payload.start_time, payload.end_time)
    now = datetime.utcnow()
    return EventOut(
        id="stub",
        owner_uid=current_user.uid,
        created_at=now,
        updated_at=now,
        reminder_minutes_before=payload.reminder_minutes_before,
        title=payload.title,
        description=payload.description,
        start_time=payload.start_time,
        end_time=payload.end_time,
        location=payload.location,
        attendees=payload.attendees or [],
    )


# PUBLIC_INTERFACE
@router.get(
    "/{event_id}",
    summary="Get event",
    response_model=EventOut,
)
def get_event(
    event_id: str = Path(..., description="ID of the event"),
    current_user: CurrentUser = Depends(verify_firebase_token),
):
    """Get a single event by ID."""
    now = datetime.utcnow()
    return EventOut(
        id=event_id,
        owner_uid=current_user.uid,
        created_at=now,
        updated_at=now,
        reminder_minutes_before=30,
        title="Sample",
        description=None,
        start_time=now,
        end_time=None,
        location=None,
        attendees=[],
    )


# PUBLIC_INTERFACE
@router.patch(
    "/{event_id}",
    summary="Update event",
    response_model=EventOut,
)
def update_event(
    event_id: str,
    payload: EventUpdate,
    current_user: CurrentUser = Depends(verify_firebase_token),
):
    """Update an existing event."""
    now = datetime.utcnow()
    return EventOut(
        id=event_id,
        owner_uid=current_user.uid,
        created_at=now,
        updated_at=now,
        reminder_minutes_before=payload.reminder_minutes_before,
        title=payload.title or "Sample",
        description=payload.description,
        start_time=payload.start_time or now,
        end_time=payload.end_time,
        location=payload.location,
        attendees=payload.attendees or [],
    )


# PUBLIC_INTERFACE
@router.delete(
    "/{event_id}",
    summary="Delete event",
    response_model=dict,
)
def delete_event(event_id: str, current_user: CurrentUser = Depends(verify_firebase_token)):
    """Delete an event by ID."""
    return {"success": True}
