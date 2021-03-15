from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base as Base
from sqlalchemy import Column, Integer, String

class DataType(Base):
    __tablename__ = 'data_type'
    code = Column(String, primary_key=True)

class PageType(Base):
    __tablename__ = 'page_type'
    code = Column(String, primary_key=True)

class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    domain = Column(String)
    robots_content = Column(String)
    sitemap_content = Column(String)

engine = create_engine('postgresql+psycopg2://postgres@0.0.0.0:5431/postgres', connect_args={'options': '-csearch_path=crawldb'})
