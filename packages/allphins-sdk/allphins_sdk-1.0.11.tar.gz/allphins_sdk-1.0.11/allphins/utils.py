import uuid
from uuid import UUID


def validate_uuid4(uuid_string: UUID | str) -> bool:
    """Validate that a UUID string is in fact a valid uuid4.

    Args
        uuid_string: The string to validate.

    Returns:
        True if uuid_string is a valid uuid4, False otherwise.
    """
    if uuid_string is None:
        return False

    if isinstance(uuid_string, uuid.UUID):
        return True

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False

    return val.hex == uuid_string.replace('-', '')
