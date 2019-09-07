import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bottle import HTTPError

DB_PATH = "sqlite:///albums.sqlite3"

Base = declarative_base()


class Album(Base):
    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.Text)
    genre = sa.Column(sa.Text)
    album = sa.Column(sa.Text)


def db_connect():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find_album(artist):
    session = db_connect()
    query = session.query(Album).filter(Album.artist == artist).all()
    albums = [alb.album for alb in query]
    return albums


def add_album(year, artist, genre, album):
    try:
        year = int(year)
        if album in find_album(artist):
            return HTTPError(409, "%s is already listed in the database" % album)
        elif 1900 < year < 2019:
            session = db_connect()
            alb = Album(
                year=year,
                artist=artist,
                genre=genre,
                album=album
            )
            session.add(alb)
            session.commit()
            return "New album is successfully added to the database"
        else:
            return HTTPError(400, "Incorrect release year. Please, write a year between 1900 and 2019")
    except ValueError as err:
        return HTTPError(400, "%s is not the year, because it is not the integer. Please, type the integer in this "
                              "attribute" % year)