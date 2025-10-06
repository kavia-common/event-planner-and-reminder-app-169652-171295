from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings, AppSettings
from .dependencies.firebase import get_firebase_app
from .routers import events as events_router
from .routers import birthdays as birthdays_router
from .routers import messages as messages_router
from .routers import profiles as profiles_router
from .routers import notifications as notifications_router

logger = logging.getLogger("uvicorn.error")


def _validate_env(settings: AppSettings) -> None:
    """Validate presence of critical env variables at startup and log clear errors."""
    required = [
        "FIREBASE_PROJECT_ID",
        "FIREBASE_CLIENT_EMAIL",
        "FIREBASE_PRIVATE_KEY",
        "FIREBASE_STORAGE_BUCKET",
        "FIREBASE_WEB_API_KEY",
        "FIREBASE_MESSAGING_SENDER_ID",
        "FIREBASE_APP_ID",
    ]
    missing = [k for k in required if not getattr(settings, k, None)]
    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        # Do not raise to allow /docs and health to render, but Firebase init will fail.
    else:
        logger.info("All required environment variables are present.")


def _try_start_scheduler() -> Optional[object]:
    """Optionally start APScheduler if a notifications service provides it."""
    try:
        # Lazy import; service may not exist yet
        from .services.notifications import start_scheduler  # type: ignore
    except Exception as exc:
        logger.info("Notifications scheduler not available or failed to import: %s", exc)
        return None

    try:
        scheduler = start_scheduler()
        logger.info("Scheduler started: %s", scheduler)
        return scheduler
    except Exception as exc:
        logger.error("Failed to start scheduler: %s", exc)
        return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI application lifespan.

    Initializes:
    - Environment validation
    - Firebase application
    - Optional APScheduler (if services.notifications.start_scheduler exists)

    Ensures graceful shutdown of scheduler if present.
    """
    settings = get_settings()
    _validate_env(settings)

    # Initialize Firebase early so dependencies can use it
    try:
        get_firebase_app()
        logger.info("Firebase app initialized.")
    except Exception as exc:
        logger.error("Firebase initialization failed: %s", exc)

    # Optional: start in-process scheduler for reminders/notifications
    scheduler = _try_start_scheduler()

    yield

    # Shutdown: stop scheduler if running
    try:
        if scheduler and hasattr(scheduler, "shutdown"):
            scheduler.shutdown(wait=False)  # type: ignore[attr-defined]
            logger.info("Scheduler shut down.")
    except Exception as exc:
        logger.warning("Error while shutting down scheduler: %s", exc)


app = FastAPI(
    title="Event Manager Backend API",
    description="Backend API for events, birthdays, messaging, profiles, and notifications powered by Firebase.",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Health", "description": "Service health and diagnostics"},
        {"name": "Events", "description": "Event CRUD and reminders"},
        {"name": "Birthdays", "description": "Birthday CRUD and reminders"},
        {"name": "Messages", "description": "Messaging threads and messages"},
        {"name": "Profiles", "description": "User profiles and FCM token management"},
        {"name": "Notifications", "description": "Notifications and scheduler operations"},
    ],
)

# CORS (permissive for dev; tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Health check endpoint to verify service availability."""
    return {"message": "Healthy"}


# Include all routers with prefixes and tags already set within the router modules
app.include_router(events_router.router)
app.include_router(birthdays_router.router)
app.include_router(messages_router.router)
app.include_router(profiles_router.router)
app.include_router(notifications_router.router)


# Optional: explicit route to surface missing envs for diagnostics (200 always)
@app.get("/_env_check", tags=["Health"], summary="Environment Check")
def env_check():
    """Diagnostic endpoint listing which critical environment variables are set."""
    settings = get_settings()
    required = [
        "FIREBASE_PROJECT_ID",
        "FIREBASE_CLIENT_EMAIL",
        "FIREBASE_PRIVATE_KEY",
        "FIREBASE_STORAGE_BUCKET",
        "FIREBASE_WEB_API_KEY",
        "FIREBASE_MESSAGING_SENDER_ID",
        "FIREBASE_APP_ID",
    ]
    status_map = {k: bool(getattr(settings, k, None)) for k in required}
    return JSONResponse(content=status_map)
