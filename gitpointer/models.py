# -*- coding: utf-8 -*-
# Copyright (C) 2010, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# License: MIT

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer, DateTime
from sqlalchemy.orm import relation, backref

from gitpointer.backend import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), index=True)
    date_checked = Column(DateTime)

class FollowingRelationship(Base):
    __tablename__ = 'following'
    id = Column(Integer, primary_key=True)
    follower = Column(Integer, ForeignKey('user.id'), index=True)
    followee = Column(Integer, ForeignKey('user.id'), index=True)
    
    def __init__(self, start, end):
        '''
        `start` follows `end`
        '''
        self.follower = start
        self.followee = end

class Repository(Base):
    __tablename__ = 'repository'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('user.id'), index=True)
    name = Column(String(255))

    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

class WatchRelationship(Base):
    __tablename__ = 'watch'
    id = Column(Integer, primary_key=True)
    watcher = Column(Integer, ForeignKey('user.id'), index=True)
    watched_repo = Column(Integer, ForeignKey('repository.id'), index=True)

