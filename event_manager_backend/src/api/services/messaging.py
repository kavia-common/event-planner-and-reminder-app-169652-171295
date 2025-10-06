from __future__ import annotations

from typing import Dict, List, Optional

# Use firebase_admin.messaging via our firebase dependency to ensure app is initialized
from ..dependencies.firebase import get_messaging_module


# PUBLIC_INTERFACE
def send_to_tokens(tokens: List[str], title: str, body: str, data: Optional[Dict[str, str]] = None) -> Dict[str, int]:
    """Send a notification to a list of FCM tokens. Returns counts of successes/failures."""
    if not tokens:
        return {"success": 0, "failure": 0}

    messaging = get_messaging_module()
    messages = [
        messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            token=token,
        )
        for token in tokens
    ]

    response = messaging.send_all(messages)
    return {"success": response.success_count, "failure": response.failure_count}


# PUBLIC_INTERFACE
def build_event_reminder_payload(event_id: str, title: str) -> Dict[str, str]:
    """Create data payload for event reminder notifications."""
    return {"type": "event_reminder", "event_id": event_id, "title": title}


# PUBLIC_INTERFACE
def build_birthday_reminder_payload(birthday_id: str, name: str) -> Dict[str, str]:
    """Create data payload for birthday reminder notifications."""
    return {"type": "birthday_reminder", "birthday_id": birthday_id, "name": name}


# PUBLIC_INTERFACE
def build_new_message_payload(thread_id: str) -> Dict[str, str]:
    """Create data payload for new message notifications."""
    return {"type": "new_message", "thread_id": thread_id}
