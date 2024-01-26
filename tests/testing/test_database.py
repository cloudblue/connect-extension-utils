from sqlalchemy.orm import scoped_session

from connect_extension_utils.testing.database import Session


def test_session():
    assert isinstance(Session, scoped_session)
