"""Initiates the db session."""

from sqlmodel import Session, create_engine
from sqlalchemy.exc import DisconnectionError, OperationalError, TimeoutError
from doplaydo.dodata_core.models import Project
from . import settings

engine = create_engine(settings.dodata_db_connection_url, echo=settings.debug)

sessions: list[Session] = []


def get_session() -> Session:
    """Get the one and only DB session."""
    if len(sessions) == 0:
        with Session(engine) as session:
            sessions.append(session)
    session = sessions[0]
    try:
        session.get(Project, 0)
    except (DisconnectionError, OperationalError, TimeoutError):
        session.close()
        with Session(engine) as session:
            sessions[0] = session
    return sessions[0]
