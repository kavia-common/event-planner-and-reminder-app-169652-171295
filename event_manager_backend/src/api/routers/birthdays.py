from __future__ import annotations

from datetime import datetime
from fastapi import APIRouter, Depends, Path, Query, status

from ..dependencies.auth import verify_firebase_token
from ..models.schemas import BirthdayCreate, BirthdayOut, BirthdayUpdate, Paginated, CurrentUser
from ..utils.pagination import parse_pagination

router = APIRouter(prefix="/birthdays", tags=["Birthdays"])


# PUBLIC_INTERFACE
@router.get("", summary="List birthdays", response_model=Paginated[BirthdayOut])
def list_birthdays(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), current_user: CurrentUser = Depends(verify_firebase_token)):
    """List birthdays for the authenticated user."""
    l, o = parse_pagination(limit, offset)
    now = datetime.utcnow()
    sample = BirthdayOut(
        id="stub",
        owner_uid=current_user.uid,
        created_at=now,
        updated_at=now,
        name="Sample",
        date=now,
        note=None,
        reminder_days_before=1,
    )
    return Paginated[BirthdayOut](items=[sample], limit=l, offset=o, total=1, next_offset=None)


# PUBLIC_INTERFACE
@router.post("", summary="Create birthday", response_model=BirthdayOut, status_code=status.HTTP_201_CREATED)
def create_birthday(payload: BirthdayCreate, current_user: CurrentUser = Depends(verify_firebase_token)):
    """Create a birthday entry."""
    now = datetime.utcnow()
    return BirthdayOut(
        id="stub",
        owner_uid=current_user.uid,
        created_at=now,
        updated_at=now,
        name=payload.name,
        date=payload.date,
        note=payload.note,
        reminder_days_before=payload.reminder_days_before,
    )


# PUBLIC_INTERFACE
@router.get("/{birthday_id}", summary="Get birthday", response_model=BirthdayOut)
def get_birthday(birthday_id: str = Path(...), current_user: CurrentUser = Depends(verify_firebase_token)):
    """Get a birthday by ID."""
    now = datetime.utcnow()
    return BirthdayOut(
        id=birthday_id,
        owner_uid=current_user.uid,
        created_at=now,
        updated_at=now,
        name="Sample",
        date=now,
        note=None,
        reminder_days_before=1,
    )


# PUBLIC_INTERFACE
@router.patch("/{birthday_id}", summary="Update birthday", response_model=BirthdayOut)
def update_birthday(birthday_id: str, payload: BirthdayUpdate, current_user: CurrentUser = Depends(verify_firebase_token)):
    """Update a birthday by ID."""
    now = datetime.utcnow()
    return BirthdayOut(
        id=birthday_id,
        owner_uid=current_user.uid,
        created_at=now,
        updated_at=now,
        name=payload.name or "Sample",
        date=payload.date or now,
        note=payload.note,
        reminder_days_before=payload.reminder_days_before,
    )


# PUBLIC_INTERFACE
@router.delete("/{birthday_id}", summary="Delete birthday", response_model=dict)
def delete_birthday(birthday_id: str, current_user: CurrentUser = Depends(verify_firebase_token)):
    """Delete a birthday by ID."""
    return {"success": True}
