from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import Header, HTTPException, status

from firebase_admin import auth as firebase_auth

from ..dependencies.firebase import get_firebase_app
from ..models.schemas import CurrentUser

# Ensure Firebase app loaded before using auth
get_firebase_app()


# PUBLIC_INTERFACE
def verify_firebase_token(authorization: Optional[str] = Header(None)) -> CurrentUser:
    """Verify Firebase ID token from Authorization header and return current user info."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

    token = authorization.split(" ", 1)[1].strip()
    try:
        decoded = firebase_auth.verify_id_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    uid: str = decoded.get("uid") or decoded.get("user_id")
    email: Optional[str] = decoded.get("email")
    name: Optional[str] = decoded.get("name")
    claims: Dict[str, Any] = {k: v for k, v in decoded.items() if k not in {"uid", "user_id", "email", "name"}}

    if not uid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    return CurrentUser(uid=uid, email=email, display_name=name, claims=claims)
