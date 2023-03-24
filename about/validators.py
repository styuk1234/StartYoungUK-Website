import os
from django.core.exceptions import ValidationError

# TODO validate these file extensions
def validate_file_extension(item):
    ext = os.path.splitext(item.name)[1]
    valid_extensions = ['.mp4', '.mov', '.docx', '.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')