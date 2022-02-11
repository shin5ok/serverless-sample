
from sqlalchemy import *
import click
import os
import logging

conn_string: str = os.environ.get("CONN")
engine = create_engine(conn_string)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

@click.group()
def cli() -> None:
    pass

@cli.command()
def dbinit() -> None:
    metadata = MetaData(bind=engine)

    singers = Table(
        "Singers",
        metadata,
        Column("SingerId", String(36), primary_key=True, nullable=False),
        Column("FirstName", String(200)),
        Column("LastName", String(200), nullable=False),
        Column("FullName", String(400), Computed("COALESCE(FirstName || ' ', '') || LastName")),
    )

    albums = Table(
        "Albums",
        metadata,
        Column("AlbumId", String(36), primary_key=True, nullable=False),
        Column("Title", String(100), nullable=False),
        Column("SingerId", String(36), ForeignKey("Singers.SingerId", name="FK_Albums_Singers"), nullable=False),
    )

    tracks = Table(
        "Tracks",
        metadata,
        Column("AlbumId", String(36), primary_key=True, nullable=False),
        Column("TrackId", Integer, primary_key=True, nullable=False),
        Column("Title", String(200), nullable=False),
        spanner_interleave_in="Albums",
        spanner_interleave_on_delete_cascade=True,
    )
    tracks.add_is_dependent_on(albums)

    metadata.create_all(engine)
    print("DB initialized")

@cli.command()
@click.option("--first_name", "-f")
@click.option("--last_name", "-l")
@click.option("--album_title", "-a")
@click.option("--track_title", "-t")
def put(first_name: str, last_name: str, album_title: str, track_title:str, init: bool) -> None:
    import uuid
    singers = Table("Singers", MetaData(bind=engine), autoload=True)
    albums = Table("Albums", MetaData(bind=engine), autoload=True)
    tracks = Table("Tracks", MetaData(bind=engine), autoload=True)

    with engine.begin() as connection:
        singer_id = str(uuid.uuid4())
        connection.execute(singers.insert(), {"SingerId": singer_id, "FirstName": first_name, "LastName": last_name})
        album_id = str(uuid.uuid4())
        connection.execute(albums.insert(), {"AlbumId": album_id, "Title": album_title, "SingerId": singer_id})
        connection.execute(tracks.insert(), {"AlbumId": album_id, "TrackId": 1, "Title": track_title})

@cli.command()
@click.option("--singer_name", "-s")
def get(singer_name: str) -> None:
    singers = Table("Singers", MetaData(bind=engine), autoload=True)
    with engine.begin() as connection:
        if singer_name:
            s = connection.execute(select([singers]).where(singers.c.FirstName == singer_name))
        else:
            s = connection.execute(select([singers]))
        for row in s:
            print(row)


if __name__ == '__main__':
    cli()