from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from hotel.db.models import Base

engine: Engine | None = None
DBSession = sessionmaker()


def init_db(file: str):
    engine = create_engine(file)
    Base.metadata.bind = engine
    DBSession.configure(bind=engine)
