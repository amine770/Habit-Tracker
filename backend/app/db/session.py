from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:    
        db.close()


