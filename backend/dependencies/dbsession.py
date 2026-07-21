# dbsession.py
from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, create_engine, text
from sqlalchemy.engine.url import make_url 
from utils.constants import DATABASE_URL, validate_constants

for value, name in [(DATABASE_URL, 'DATABASE_URL')]:
    validate_constants(value, name)

# echo=True -> imprime las consultas SQL en la consola.
engine = create_engine(DATABASE_URL, echo=False)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]