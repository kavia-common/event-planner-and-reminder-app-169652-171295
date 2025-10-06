from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from ..dependencies.auth import verify_firebase_token
from ..models.schemas import SuccessResponse, CurrentUser

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# PUBLIC_INTERFACE
@router.get("/test", summary="Send test notification", response_model=SuccessResponse)
def send_test_notification(title: str = Query("Hello"), body: str = Query("World"), current_user: CurrentUser = Depends(verify_firebase_token)):
    """Send a test notification to all of the user's registered tokens (stub)."""
    return SuccessResponse(success=True, message=f"Would send '{title}: {body}' to {current_user.uid}")
