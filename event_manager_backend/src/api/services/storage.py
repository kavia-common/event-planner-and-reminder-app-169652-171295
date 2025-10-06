from __future__ import annotations

import mimetypes
from datetime import timedelta

from fastapi import UploadFile

from ..dependencies.firebase import get_storage_bucket


# PUBLIC_INTERFACE
async def upload_profile_photo(file: UploadFile, uid: str) -> str:
    """Upload profile photo to Firebase Storage and return a public download URL."""
    bucket = get_storage_bucket()
    ext = ""
    if file.filename and "." in file.filename:
        ext = "." + file.filename.rsplit(".", 1)[1].lower()
    path = f"profiles/{uid}/photo{ext or ''}"

    blob = bucket.blob(path)
    content_type = file.content_type or mimetypes.guess_type(file.filename or "")[0] or "application/octet-stream"

    # Upload
    blob.upload_from_file(file.file, content_type=content_type)

    # Generate a signed URL for temporary public access
    url = blob.generate_signed_url(expiration=timedelta(days=7), method="GET")
    return url
