from __future__ import annotations

from fastapi import APIRouter, Depends, UploadFile, File

from ..dependencies.auth import verify_firebase_token
from ..models.schemas import ProfileOut, ProfileUpdate, CurrentUser, SuccessResponse

router = APIRouter(prefix="/profiles", tags=["Profiles"])


# PUBLIC_INTERFACE
@router.get("/me", summary="Get my profile", response_model=ProfileOut)
def get_my_profile(current_user: CurrentUser = Depends(verify_firebase_token)):
    """Get the authenticated user's profile."""
    return ProfileOut(uid=current_user.uid, email=current_user.email, display_name=current_user.display_name, photo_url=None, fcm_tokens=[])


# PUBLIC_INTERFACE
@router.patch("/me", summary="Update my profile", response_model=ProfileOut)
def update_my_profile(payload: ProfileUpdate, current_user: CurrentUser = Depends(verify_firebase_token)):
    """Update the authenticated user's profile."""
    return ProfileOut(uid=current_user.uid, email=current_user.email, display_name=payload.display_name or current_user.display_name, photo_url=payload.photo_url, fcm_tokens=[])


# PUBLIC_INTERFACE
@router.post("/me/photo", summary="Upload profile photo", response_model=ProfileOut)
async def upload_my_photo(file: UploadFile = File(...), current_user: CurrentUser = Depends(verify_firebase_token)):
    """Upload a new profile photo for the authenticated user."""
    # In real implementation we would call services.storage.upload_profile_photo
    return ProfileOut(uid=current_user.uid, email=current_user.email, display_name=current_user.display_name, photo_url="https://example.com/photo.jpg", fcm_tokens=[])


# PUBLIC_INTERFACE
@router.post("/me/fcm/register", summary="Register FCM token", response_model=SuccessResponse)
def register_fcm_token(token: str, current_user: CurrentUser = Depends(verify_firebase_token)):
    """Register an FCM token for push notifications."""
    return SuccessResponse(success=True, message=f"Registered token {token}")


# PUBLIC_INTERFACE
@router.post("/me/fcm/unregister", summary="Unregister FCM token", response_model=SuccessResponse)
def unregister_fcm_token(token: str, current_user: CurrentUser = Depends(verify_firebase_token)):
    """Unregister an FCM token."""
    return SuccessResponse(success=True, message=f"Unregistered token {token}")
