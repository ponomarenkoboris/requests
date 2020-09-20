import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()# класс используется для описания декларативный моделей таблиц в бфзе данных

class Album():
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки.
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к БД, создаёт таблицы, если их ещё нет и возвращает объект сессии.
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    """
    Находит все альбомы в бд по заданному артисту.
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def save_user_info(year, artist, genre, album):
    assert isinstance(year, int)#проверяет принадлежность данных
    assert isinstance(artist, str)
    assert isinstance(genre, str)
    assert isinstance(album, str)

    session = connect_db()
    saved_alubm = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if saved_alubm is not None:
        raise AlreadyExists(f"Альбом уже существует {saved_alubm.id}")

    album = Album(year=year, artist=artist, genre=genre, album=album)
    session.add(album)
    session.commit()
    return album