from contextlib import contextmanager

from sqlmodel import Session


@contextmanager
def transaction_scope(db: Session):
    """Context manager for handling database transactions."""
    try:
        yield
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
