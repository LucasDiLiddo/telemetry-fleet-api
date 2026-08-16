from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Para SQLite necesitamos desactivar check_same_thread
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False  # Cambiar a True si querés ver las queries SQL crudas en consola
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Inyector de dependencia para FastAPI: abre y cierra la sesión de BD por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()