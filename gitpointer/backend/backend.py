# -*- coding: utf-8 -*-
# Copyright (C) 2010, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# License: MIT

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import path

_paths = [
    path.join(path.abspath(path.dirname(__file__)), '..', '..'),
    '.',
    ]
database_file = 'gitpointer.sqlite3'
for _basep in _paths:
    _fullp = path.join(_basep, database_file)
    if path.exists(_fullp):
        database_file = _fullp

Base = declarative_base()
engine = create_engine('sqlite:///' + database_file, echo=False)
metadata = Base.metadata
metadata.bind = engine
create_session = sessionmaker(bind=engine)

def create_tables():
    '''
    create_tables()

    Creates all tables in database.
    '''
    metadata.create_all()

