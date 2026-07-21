# dbsession.py
from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, create_engine, text
from sqlalchemy.engine.url import make_url 
from utils.constants import DATABASE_URL, NAME_DB, validate_constants

for value, name in [(DATABASE_URL, 'DATABASE_URL'), (NAME_DB, 'NAME_DB')]:
    validate_constants(value, name)

# echo=True -> imprime las consultas SQL en la consola.
engine = create_engine(DATABASE_URL, echo=False)

def create_database_postgresql_native(url_base: str = DATABASE_URL, namedb: str = NAME_DB):
    """
    url_base: Ej. "postgresql://postgres:password@localhost:5432/postgres"
    """

    url = make_url(url_base)
    
    admin_url = url.set(database="postgres")
    
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    
    try:
        with admin_engine.connect() as conn:
          
            check_db = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{namedb}'")).scalar()
            
            if not check_db:
                conn.execute(text(f"CREATE DATABASE {namedb}"))
                print(f"[+] Creación completada de la Base de Datos ({namedb}) en PostgreSQL")
            else:
                print(f"[*] La base de datos ({namedb}) ya existe.")
    except Exception as e:
        print(f"[-] Surgió un Problema: {e}")
        raise ValueError("No se creó la base de datos")

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]