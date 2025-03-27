import uuid


def generate_uuid():
    return str(uuid.uuid4())


def is_uuid(string: str | None) -> bool:
    if not string:
        return False
    try:
        uuid.UUID(string)
        return True
    except ValueError:
        return False
