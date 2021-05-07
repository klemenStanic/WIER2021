"""
To init database connect to it using the following command and then run CREATE TABLE statements.
sqlite3 inverted-index.db

CREATE TABLE IndexWord (
  word TEXT PRIMARY KEY
);

CREATE TABLE Posting (
  word TEXT NOT NULL,
  documentName TEXT NOT NULL,
  frequency INTEGER NOT NULL,
  indexes TEXT NOT NULL,
  PRIMARY KEY(word, documentName),
  FOREIGN KEY (word) REFERENCES IndexWord(word)
);
"""

from sqlalchemy import create_engine, Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()
engine = create_engine('sqlite:///inverted-index.db')


class IndexWord(Base):
    __tablename__ = 'IndexWord'
    word = Column('word', String, primary_key=True)


class Posting(Base):
    __tablename__ = 'Posting'
    word = Column('word', String, ForeignKey(IndexWord.word), primary_key=True)
    document_name = Column('documentName', String, primary_key=True)
    frequency = Column('frequency', Integer)
    indexes = Column('indexes', String)


if __name__ == '__main__':
    session = Session(engine)
    resp = session.query(IndexWord).first()
    print(resp)
    session.close()

