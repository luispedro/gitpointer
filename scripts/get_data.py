# -*- coding: utf-8 -*-
# Copyright (C) 2010, Luis Pedro Coelho <luis@luispedro.org>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# License: MIT

import itertools
from time import sleep

from github2.client import Github

def maybe_mkdir(d):
    from os import mkdir, errno
    try:
        mkdir(d)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

github = Github()

seed = u'luispedro'
queue = [seed]
seen = set(queue)
while queue:
    sleep(5)
    user = queue.pop()
    following = github.users.following(user)
    followers = github.users.followers(user)
    maybe_mkdir('database/' + user[:3])
    output = file('database/%s/%s' % (user[:3], user), 'w')
    for f in following:
        print >>output, f
    print >>output
    for f in followers:
        print >>output, f
    output.close()
    for u in itertools.chain(following, followers):
        if u not in seen:
            seen.add(u)
            queue.append(u)
    print "seen: %s (queue: %s)" % (len(seen), len(queue))

