from __future__ import annotations

import threading
from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore, storage, messaging

from ..config import get_settings

# Thread-safe initialization
_init_lock = threading.Lock()


# PUBLIC_INTERFACE
def get_firebase_app() -> firebase_admin.App:
    """Return a lazily initialized singleton Firebase app using env-based service account."""
    app = firebase_admin.get_app() if _has_default_app() else None
    if app:
        return app

    with _init_lock:
        if _has_default_app():
            return firebase_admin.get_app()
        settings = get_settings()
        cred_dict = {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key_id": "ignored-in-env",
            "private_key": settings.private_key_with_newlines(),
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "client_id": "ignored-in-env",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{settings.FIREBASE_CLIENT_EMAIL}",
            "universe_domain": "googleapis.com",
        }
        cred = credentials.Certificate(cred_dict)
        return firebase_admin.initialize_app(cred, {"storageBucket": settings.FIREBASE_STORAGE_BUCKET})


def _has_default_app() -> bool:
    try:
        firebase_admin.get_app()
        return True
    except ValueError:
        return False


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_firestore() -> firestore.Client:
    """Return Firestore client for the default app."""
    app = get_firebase_app()
    return firestore.client(app=app)


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_storage_bucket() -> storage.bucket.Bucket:
    """Return Firebase Storage bucket for the default app."""
    app = get_firebase_app()
    return storage.bucket(app=app)


# PUBLIC_INTERFACE
def get_messaging_module() -> messaging:
    """Expose messaging module from firebase_admin.messaging."""
    # Ensure app is initialized before using messaging send APIs
    get_firebase_app()
    return messaging
