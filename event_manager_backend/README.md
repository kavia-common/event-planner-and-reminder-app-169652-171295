# Event Manager Backend (FastAPI + Firebase)

This backend powers the Event Planner and Reminder App. It integrates with Firebase for authentication, Firestore for data storage, Cloud Storage for media, and FCM for push notifications.

## Features
- User authentication via Firebase ID tokens
- Events: CRUD and scheduled reminders
- Birthdays: CRUD and scheduled reminders
- Messaging: threads and messages with push notifications
- Profiles: get/update, profile photo upload, FCM token registration
- OpenAPI docs at /docs

## Requirements
- Python 3.11+
- Firebase project with:
  - Service account (private key)
  - Firestore (Native mode)
  - Cloud Storage bucket
  - Cloud Messaging enabled
- Firebase CLI installed (https://firebase.google.com/docs/cli)

## Setup
1. Create and activate virtual environment
2. Install dependencies  
   pip install -r requirements.txt
3. Create a .env file in this directory based on .env.example and fill values from your Firebase Console.

Notes:
- FIREBASE_PRIVATE_KEY must be stored with escaped newlines (\\n) when placed into .env.

## Run (development)
- Start the API:  
  uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

- Visit:  
  http://localhost:3001/docs

## OpenAPI
To regenerate interfaces/openapi.json locally:  
  python -m src.api.generate_openapi

## Security and Rules
We ship least-privilege Firestore and Storage rules alongside the backend. Review and deploy them using Firebase CLI.

Rules files (paths relative to this directory):
- Firestore rules: firebase.security.rules
- Storage rules: storage.rules

### Set Firebase project
If you have multiple projects, select the target project:
  firebase use <your-project-id>

Or set the project explicitly per command:
  firebase --project <your-project-id> <command>

### Deploy rules
Deploy Firestore rules:
  firebase deploy --only firestore:rules

Deploy Storage rules:
  firebase deploy --only storage:rules

If your firebase.json uses custom paths, make sure it points to:
- firestore.rules: "event_manager_backend/firebase.security.rules"
- storage.rules: "event_manager_backend/storage.rules"

Example firebase.json snippet at repo root:
{
  "firestore": { "rules": "event_manager_backend/firebase.security.rules" },
  "storage": { "rules": "event_manager_backend/storage.rules" }
}

## Environment Variables
See .env.example for the full list and how to obtain them.

## Notes
- CORS is permissive for development; tighten before production.
- Scheduler (APScheduler) runs in-process; for production, use a single instance or external scheduling to avoid duplicate sends.

## API Quickstart (curl/HTTPie)
Replace AUTH with a valid Firebase ID token: export AUTH="Bearer eyJhbGciOi..."

- Health
  curl -s http://localhost:3001/
  http :3001/

- Events
  # List
  curl -s -H "Authorization: $AUTH" "http://localhost:3001/events?limit=10&offset=0"
  http GET :3001/events "Authorization:$AUTH"

  # Create
  curl -s -X POST -H "Authorization: $AUTH" -H "Content-Type: application/json" \
    -d '{"title":"Meeting","start_time":"2025-01-01T10:00:00Z","end_time":"2025-01-01T11:00:00Z","attendees":["uid2"],"reminder_minutes_before":30}' \
    http://localhost:3001/events
  http POST :3001/events "Authorization:$AUTH" title=Meeting start_time=2025-01-01T10:00:00Z end_time=2025-01-01T11:00:00Z attendees:='["uid2"]' reminder_minutes_before:=30

  # Get
  curl -s -H "Authorization: $AUTH" http://localhost:3001/events/evt123
  http GET :3001/events/evt123 "Authorization:$AUTH"

  # Update
  curl -s -X PATCH -H "Authorization: $AUTH" -H "Content-Type: application/json" -d '{"title":"Updated"}' http://localhost:3001/events/evt123
  http PATCH :3001/events/evt123 "Authorization:$AUTH" title=Updated

  # Delete
  curl -s -X DELETE -H "Authorization: $AUTH" http://localhost:3001/events/evt123
  http DELETE :3001/events/evt123 "Authorization:$AUTH"

- Birthdays
  # List
  curl -s -H "Authorization: $AUTH" "http://localhost:3001/birthdays?limit=10&offset=0"
  http GET :3001/birthdays "Authorization:$AUTH"

  # Create
  curl -s -X POST -H "Authorization: $AUTH" -H "Content-Type: application/json" \
    -d '{"name":"Alice","date":"2025-01-01T00:00:00Z","note":"Friend","reminder_days_before":3}' \
    http://localhost:3001/birthdays
  http POST :3001/birthdays "Authorization:$AUTH" name=Alice date=2025-01-01T00:00:00Z note=Friend reminder_days_before:=3

  # Get
  curl -s -H "Authorization: $AUTH" http://localhost:3001/birthdays/b123
  http GET :3001/birthdays/b123 "Authorization:$AUTH"

  # Update
  curl -s -X PATCH -H "Authorization: $AUTH" -H "Content-Type: application/json" -d '{"note":"Best friend"}' http://localhost:3001/birthdays/b123
  http PATCH :3001/birthdays/b123 "Authorization:$AUTH" note='Best friend'

  # Delete
  curl -s -X DELETE -H "Authorization: $AUTH" http://localhost:3001/birthdays/b123
  http DELETE :3001/birthdays/b123 "Authorization:$AUTH"

- Messages
  # List threads
  curl -s -H "Authorization: $AUTH" "http://localhost:3001/messages/threads?limit=10&offset=0"
  http GET :3001/messages/threads "Authorization:$AUTH"

  # List messages in a thread
  curl -s -H "Authorization: $AUTH" "http://localhost:3001/messages/threads/t123/messages?limit=10&offset=0"
  http GET :3001/messages/threads/t123/messages "Authorization:$AUTH"

  # Send message
  curl -s -X POST -H "Authorization: $AUTH" -H "Content-Type: application/json" -d '{"thread_id":"t123","content":"Hello"}' http://localhost:3001/messages/send
  http POST :3001/messages/send "Authorization:$AUTH" thread_id=t123 content=Hello

- Profiles
  # Get my profile
  curl -s -H "Authorization: $AUTH" http://localhost:3001/profiles/me
  http GET :3001/profiles/me "Authorization:$AUTH"

  # Update my profile
  curl -s -X PATCH -H "Authorization: $AUTH" -H "Content-Type: application/json" -d '{"display_name":"New Name"}' http://localhost:3001/profiles/me
  http PATCH :3001/profiles/me "Authorization:$AUTH" display_name='New Name'

  # Register FCM token
  curl -s -X POST -H "Authorization: $AUTH" "http://localhost:3001/profiles/me/fcm/register?token=abc123"
  http POST :3001/profiles/me/fcm/register "Authorization:$AUTH" token=abc123

  # Unregister FCM token
  curl -s -X POST -H "Authorization: $AUTH" "http://localhost:3001/profiles/me/fcm/unregister?token=abc123"
  http POST :3001/profiles/me/fcm/unregister "Authorization:$AUTH" token=abc123

- Notifications
  # Test notification
  curl -s -H "Authorization: $AUTH" "http://localhost:3001/notifications/test?title=Hi&body=There"
  http GET :3001/notifications/test "Authorization:$AUTH" title==Hi body==There
