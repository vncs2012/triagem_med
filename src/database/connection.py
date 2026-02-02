import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base
from ..config import Settings

logger = logging.getLogger(__name__)

class DatabaseConnection():
    def __init__(self):
        self._engine = None
        self._sessionLocal = None
        self._session = None
        self.settings = Settings()


    def get_engine(self) -> Engine:
        if self._engine is None:
            
            db_path = self.settings.get_database_path()
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            self._engine = create_engine(
                self.settings.database_url,
                connect_args={"check_same_thread": False}
            )
            
            @event.listens_for(self._engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
            
            logger.info(f"Engine criada: {self.settings.database_url}")
        
        return self._engine


    def get_session_factory(self) -> sessionmaker:
        if self._sessionLocal is None:
            engine = self.get_engine()
            self._sessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine
            )
        
        return self._sessionLocal


    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        SessionLocal = self.get_session_factory()
        session = SessionLocal()
        
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro na sessão: {e}")
            raise
        finally:
            session.close()


    def init_database(self):
        engine = self.get_engine()
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado")


    def drop_database(self):
        engine = self.get_engine()
        Base.metadata.drop_all(bind=engine)
        logger.warning("Todas as tabelas foram removidas")


    def reset_database(self):
        self.drop_database()
        self.init_database()
        logger.info("Banco de dados resetado")
