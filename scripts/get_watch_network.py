# -*- coding: utf-8 -*-
# Copyright (C) 2010, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# License: MIT

from time import sleep
from os.path import exists
from github2.client import Github

import gitpointer.backend
from gitpointer.models import User, WatchRelationship, Repository

def maybe_mkdir(d):
    from os import mkdir, errno
    try:
        mkdir(d)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

def output_watch_text(user, repos):
    maybe_mkdir('database/' + user[:3])
    output = file('database/%s/%s.watching' % (user[:3], user), 'w')
    for r in repos:
        print >>output, '%s/%s' % (r.owner,r.name)
    output.close()
    
github = Github()
session = gitpointer.backend.create_session()
users = session.query(User).all()
queue = len(users)
for u in users:
    if exists('database/%s/%s.watching' % (u.username[:3], u.username)):
        queue -= 1
        continue
    try:
        repos = github.repos.watching(u.username)
    except RuntimeError, e:
        if e.args[0].find('404') > 0:
            continue
        print 'Error for user: %s' % u
    except:
        print 'Error for user: %s' % u
    output_watch_text(u.username, repos)
    for r in repos:
        repo = session.query(Repository) \
                    .filter_by(owner=r.owner, name=r.name).first()
        if repo is None:
            repo = Repository(r.owner, r.name, r.pushed_at)
            session.add(repo)
        session.add(WatchRelationship(u.id, repo.id))
    session.commit()
    queue -= 1
    print 'todo:', queue
    sleep(2)

