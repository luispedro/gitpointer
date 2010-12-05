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
users = session.query(User).values(User.username, User.id)
for username,uid in users:
    if exists('database/%s/%s.watching' % (username[:3], username)):
        continue
    try:
        repos = github.repos.watching(username)
    except RuntimeError, e:
        if e.args[0].find('404') > 0:
            print 'Error 404 for user: %s: %s' % (username, e)
        print 'Error for user: %s: %s' % (username, e)
        continue
    except:
        print 'Error for user: %s: %s' % (username, e)
        continue
    output_watch_text(username, repos)
    for r in repos:
        repo = session.query(Repository) \
                    .filter_by(owner=r.owner, name=r.name).first()
        if repo is None:
            repo = Repository(r.owner, r.name, r.pushed_at)
            session.add(repo)
        session.add(WatchRelationship(uid, repo.id))
    session.commit()
    print 'done', username
    sleep(2)

