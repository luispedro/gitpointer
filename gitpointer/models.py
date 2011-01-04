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
    #following = relation('FollowingRelationship', backref='followee')
    #followers = relation('FollowingRelationship', backref='follower')

    def __init__(self, username, date_checked):
        self.username = username
        self.date_checked = date_checked

class FollowingRelationship(Base):
    __tablename__ = 'following'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'), index=True)
    followee_id = Column(Integer, ForeignKey('user.id'), index=True)

    follower = relation(User, primaryjoin=(User.id == follower_id))
    followee = relation(User, primaryjoin=(User.id == followee_id))

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
    pushed_at = Column(DateTime)

    def __init__(self, owner, name, pushed_at):
        self.owner = owner
        self.name = name
        self.pushed_at = pushed_at

class WatchRelationship(Base):
    __tablename__ = 'watch'
    id = Column(Integer, primary_key=True)
    watcher_id = Column(Integer, ForeignKey('user.id'), index=True)
    watched_repo_id = Column(Integer, ForeignKey('repository.id'), index=True)
    date_checked = Column(DateTime)

    watcher = relation(User, primaryjoin=(User.id == watcher_id))
    watched_repo = relation(Repository, primaryjoin=(Repository.id == watched_repo_id))

    def __init__(self, watcher, watched_repo):
        self.watcher = watcher
        self.watched_repo = watched_repo


