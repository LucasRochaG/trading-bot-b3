
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from engine.persistence.models import Base


def init_db(database_url: str):
    """
    Inicializa o banco de dados.

    SQLite é usado no MVP.
    Futuramente podemos trocar para PostgreSQL/TimescaleDB
    sem alterar a estrutura principal do robô.
    """

    engine = create_engine(database_url)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    return Session
