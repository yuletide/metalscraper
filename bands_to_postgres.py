import scraperwiki
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.sql import select
# from geoalchemy2 import Geometry
# from sqlalchemy.orm import sessionmaker

scraper_engine = create_engine('sqlite:///scraperwiki.sqlite', echo=True)
scraper_connect = scraper_engine.connect()
scraper_metadata = MetaData()
scraper = Table('swdata', scraper_metadata, autoload=True,
                autoload_with=scraper_engine)
# scraper_session = sessionmaker(sqlite_engine)
# print(scraper.columns)
swdata = scraper_metadata.tables['swdata']
print(repr(swdata))

pg_engine = create_engine(
    'postgresql://postgres@localhost/postgres', echo=True)
scraper_metadata.create_all(pg_engine)
# pg_session - sessionmaker(pg_engine)


def get_geocoded_bands(limit=''):
    if limit:
        limit = " LIMIT " + str(limit)
    return scraperwiki.sqlite.select("* FROM swdata where geo_geom IS NOT NULL and geo_place_name <> '-1'" + limit)
