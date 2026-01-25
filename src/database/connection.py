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
        """
        Retorna a engine do SQLAlchemy.
        Cria a engine se ainda não existir.
        """
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
        """
        Retorna a factory de sessões.
        """
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
        """
        Context manager para obter uma sessão do banco de dados.
        """
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
        """
        Inicializa o banco de dados criando todas as tabelas.
        """
        engine = self.get_engine()
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado")


    def drop_database(self):
        """
        Remove todas as tabelas do banco de dados.
        """
        engine = self.get_engine()
        Base.metadata.drop_all(bind=engine)
        logger.warning("Todas as tabelas foram removidas")


    def reset_database(self):
        """
        Reseta o banco de dados (drop + create).
        """
        self.drop_database()
        self.init_database()
        logger.info("Banco de dados resetado")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Testando conexão com banco de dados...")
    database = DatabaseConnection()
    database.init_database()
    
    with database.get_session() as session:
        from sqlalchemy import inspect
        inspector = inspect(database.get_engine())
        tables = inspector.get_table_names()
        print(f"Tabelas criadas: {tables}")
    
    print("Teste concluído!")
