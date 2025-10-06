from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query, status

from ..dependencies.auth import verify_firebase_token
from ..models.schemas import MessageCreate, MessageOut, ThreadOut, CurrentUser, Paginated
from ..utils.pagination import parse_pagination

router = APIRouter(prefix="/messages", tags=["Messages"])


# PUBLIC_INTERFACE
@router.get("/threads", summary="List threads", response_model=Paginated[ThreadOut])
def list_threads(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), current_user: CurrentUser = Depends(verify_firebase_token)):
    """List message threads for the user."""
    l, o = parse_pagination(limit, offset)
    now = datetime.utcnow()
    sample_thread = ThreadOut(id="thread-stub", participants=[current_user.uid], last_message=None, unread_count=0, updated_at=now)
    return Paginated[ThreadOut](items=[sample_thread], limit=l, offset=o, total=1, next_offset=None)


# PUBLIC_INTERFACE
@router.get("/threads/{thread_id}/messages", summary="List messages in thread", response_model=Paginated[MessageOut])
def list_messages(thread_id: str, limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), current_user: CurrentUser = Depends(verify_firebase_token)):
    """List messages inside a thread."""
    l, o = parse_pagination(limit, offset)
    now = datetime.utcnow()
    sample_msg = MessageOut(id="msg-stub", sender_uid=current_user.uid, content="Hello!", sent_at=now)
    return Paginated[MessageOut](items=[sample_msg], limit=l, offset=o, total=1, next_offset=None)


# PUBLIC_INTERFACE
@router.post("/send", summary="Send message", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
def send_message(payload: MessageCreate, current_user: CurrentUser = Depends(verify_firebase_token)):
    """Send a message to a thread or create a new thread."""
    now = datetime.utcnow()
    return MessageOut(id="msg-stub", sender_uid=current_user.uid, content=payload.content, sent_at=now)
