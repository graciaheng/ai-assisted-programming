"""Saving files that users upload: the subject of DIY 4.

save_upload(filename, data) stores the bytes a user uploaded, under the
name the user's browser sent, in UPLOAD_DIR.
"""
import os

UPLOAD_DIR = "uploads"


def save_upload(filename, data):
    """Save the uploaded bytes in UPLOAD_DIR and return the path written."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    name = os.path.basename(filename)
    if not name or name in {".", ".."} or os.path.isabs(filename) or filename != name:
        raise ValueError("invalid filename")
    path = os.path.join(UPLOAD_DIR, name)
    real_dir = os.path.realpath(UPLOAD_DIR)
    real_path = os.path.realpath(path)
    if os.path.commonpath([real_dir, real_path]) != real_dir:
        raise ValueError("invalid filename")
    f = open(path, "wb")
    f.write(data)
    f.close()
    return path
