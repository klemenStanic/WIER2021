from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Text, BigInteger, LargeBinary

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://postgres@0.0.0.0:5431/postgres', connect_args={'options': '-csearch_path=crawldb'})

class DataType(Base):
    __tablename__ = 'data_type'
    code = Column('code', String, primary_key=True)

class PageType(Base):
    __tablename__ = 'page_type'
    code = Column('code', String, primary_key=True)

class Site(Base):
    __tablename__ = 'site'
    id = Column('id', Integer, primary_key=True)
    domain = Column('domain', String)
    robots_content = Column('robots_content', String)
    sitemap_content = Column('sitemap_content', String)
    site_ip = Column('site_ip', String)
    timestamp = Column('timestamp', BigInteger)
    done = Column('done', Boolean)

class Page(Base):
    __tablename__ = 'page'
    id = Column('id', Integer, primary_key=True)
    site_id = Column('site_id', Integer, ForeignKey(Site.id))
    page_type_code = Column('page_type_code', String, ForeignKey(PageType.code))
    url = Column('url', String) 
    html_content = Column('html_content', Text)
    content_hash = Column('content_hash', String)
    http_status_code = Column('http_status_code', Integer)
    accessed_time = Column('accessed_time', DateTime)

class PageData(Base):
    __tablename__ = 'page_data'
    id = Column('id', Integer, primary_key=True)
    page_id = Column('page_id', Integer, ForeignKey(Page.id))
    data_type_code = Column('data_type_code', String, ForeignKey(DataType.code))
    data = Column('data', LargeBinary)
    
class Image(Base):
    __tablename__ = 'image'
    id = Column('id', Integer, primary_key=True)
    page_id = Column('page_id', Integer, ForeignKey(Page.id))
    filename = Column('filename', String)
    content_type = Column('content_type', String)
    data = Column('data', LargeBinary)
    accessed_time = Column('accessed_time', DateTime)

class Link(Base):
    __tablename__ = 'link'
    from_page = Column('from_page', Integer, ForeignKey(Page.id), primary_key=True)
    to_page = Column('to_page', Integer, ForeignKey(Page.id), primary_key=True)

# session = Session(engine)
# print([i.code for i in session.query(DataType).all()])
