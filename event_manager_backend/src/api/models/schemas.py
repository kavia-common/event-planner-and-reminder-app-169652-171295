from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field, EmailStr


# Core user model from auth dependency
class CurrentUser(BaseModel):
    uid: str = Field(..., description="Firebase auth UID for the current user")
    email: Optional[EmailStr] = Field(None, description="User email if available")
    display_name: Optional[str] = Field(None, description="Display name from token")
    claims: Dict[str, Any] = Field(default_factory=dict, description="Custom claims from token")


# Events
class EventBase(BaseModel):
    title: str = Field(..., description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    start_time: datetime = Field(..., description="Event start time in ISO8601 (UTC recommended)")
    end_time: Optional[datetime] = Field(None, description="Event end time in ISO8601 (UTC recommended)")
    location: Optional[str] = Field(None, description="Event location")
    attendees: List[str] = Field(default_factory=list, description="List of attendee UIDs")


class EventCreate(EventBase):
    reminder_minutes_before: Optional[int] = Field(30, description="Reminder minutes before start; null to disable")


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    attendees: Optional[List[str]] = None
    reminder_minutes_before: Optional[int] = Field(None, description="Update reminder minutes; null to disable")


class EventOut(EventBase):
    id: str = Field(..., description="Event document ID")
    owner_uid: str = Field(..., description="Owner UID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    reminder_minutes_before: Optional[int] = Field(None, description="Configured reminder minutes before start")


# Birthdays
class BirthdayBase(BaseModel):
    name: str = Field(..., description="Name of the person")
    date: datetime = Field(..., description="Birthday date; time component ignored")
    note: Optional[str] = Field(None, description="Optional note")


class BirthdayCreate(BirthdayBase):
    reminder_days_before: Optional[int] = Field(1, description="Days before to remind; null to disable")


class BirthdayUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[datetime] = None
    note: Optional[str] = None
    reminder_days_before: Optional[int] = None


class BirthdayOut(BirthdayBase):
    id: str = Field(..., description="Birthday document ID")
    owner_uid: str = Field(..., description="Owner UID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    reminder_days_before: Optional[int] = Field(None, description="Configured days before birthday to remind")


# Messaging
class MessageCreate(BaseModel):
    thread_id: Optional[str] = Field(None, description="Thread ID to post into, if existing")
    recipients: Optional[List[str]] = Field(None, description="Recipients for new thread (UIDs)")
    content: str = Field(..., description="Message content text")


class MessageOut(BaseModel):
    id: str = Field(..., description="Message ID")
    sender_uid: str = Field(..., description="Sender UID")
    content: str = Field(..., description="Content text")
    sent_at: datetime = Field(..., description="Sent timestamp")


class ThreadOut(BaseModel):
    id: str = Field(..., description="Thread ID")
    participants: List[str] = Field(..., description="UIDs of participants")
    last_message: Optional[MessageOut] = Field(None, description="Last message metadata")
    unread_count: Optional[int] = Field(None, description="Unread count for current user")
    updated_at: datetime = Field(..., description="Last update timestamp")


# Profiles
class ProfileUpdate(BaseModel):
    display_name: Optional[str] = Field(None, description="Display name")
    photo_url: Optional[str] = Field(None, description="Profile photo URL")
    fcm_token: Optional[str] = Field(None, description="FCM device token to register/unregister")
    unregister_fcm_token: Optional[str] = Field(None, description="FCM token to remove")


class ProfileOut(BaseModel):
    uid: str = Field(..., description="User UID")
    email: Optional[EmailStr] = Field(None, description="Email")
    display_name: Optional[str] = Field(None, description="Display name")
    photo_url: Optional[str] = Field(None, description="Photo URL")
    fcm_tokens: List[str] = Field(default_factory=list, description="Registered FCM tokens")


# Generic responses
class SuccessResponse(BaseModel):
    success: bool = Field(True, description="Operation success flag")
    message: Optional[str] = Field(None, description="Description message")


T = TypeVar("T")


class Paginated(BaseModel, Generic[T]):
    items: List[T] = Field(default_factory=list, description="Items for current page")
    limit: int = Field(..., description="Requested limit")
    offset: int = Field(..., description="Requested offset")
    total: Optional[int] = Field(None, description="Optional total count")
    next_offset: Optional[int] = Field(None, description="Offset for next page if available")
