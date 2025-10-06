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

## Setup
1. Create and activate virtual environment
2. Install dependencies
   pip install -r requirements.txt

3. Create a .env file in this directory based on .env.example and fill values from your Firebase Console.

Notes:
- FIREBASE_PRIVATE_KEY must be stored with escaped newlines (\n) when placed into .env.

## Run (development)
- Start the API:
  uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

- Visit:
  http://localhost:3001/docs

## OpenAPI
To regenerate interfaces/openapi.json locally:
  python -m src.api.generate_openapi

## Security and Rules
- Enforce Firestore and Storage security with Firebase rules.
- Deploy rules using Firebase CLI (not covered here). Ensure backend access aligns with mobile client security posture.

## Environment Variables
See .env.example for the full list and how to obtain them.

## Notes
- CORS is permissive for development; tighten before production.
- Scheduler (APScheduler) runs in-process; for production, use a single instance or external scheduling to avoid duplicate sends.
