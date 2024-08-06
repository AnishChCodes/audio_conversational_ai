from apiflask import Schema
from apiflask.fields import File
from apiflask.validators import FileType, FileSize
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest


def validate_file(files):
    if 'audio_file' not in files:
        raise BadRequest(f"Please send a valid file")

    file = files['audio_file']

    allowed_extensions = {'mp3'}
    max_size = 5 * 1024 * 1024  # 5 MB

    if not file.filename.split('.')[-1] in allowed_extensions:
        raise BadRequest(f"Invalid file type. Allowed types are: {', '.join(allowed_extensions)}")

    if file.content_length > max_size:
        raise BadRequest("File too large. Maximum size is 5MB.")
