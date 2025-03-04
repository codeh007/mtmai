import uuid


def generate_uuid():
    return str(uuid.uuid4())


def is_uuid(string: str) -> bool:
    try:
        uuid.UUID(string)
        return True
    except ValueError:
        return False
