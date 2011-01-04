import os
from os import path
from datetime import datetime

from gitpointer.models import User, Repository, FollowingRelationship, WatchRelationship
from gitpointer.github import owner_name_of

def read_user(fname):
    username = path.basename(fname)
    username = username[:-len('.follow')]
    date_checked = datetime.fromtimestamp(int(os.stat(fname).st_mtime))
    following = []
    for line in file(fname):
        line = line.strip()
        if not line:
            break
        following.append(line)
    return username, date_checked, following

def upload_user(username, date_checked, following, create_session=None):
    if create_session is None:
        import gitpointer.backend
        create_session = gitpointer.backend.create_session
    session = create_session()
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        user = User(username, date_checked)
    else:
        user.date_checked = date_checked
    session.add(user)
    for f in following:
        user2 = session.query(User).filter(User.username == f).first()
        if user2 is None:
            user2 = User(f, None)
            session.add(user2)
        session.add(FollowingRelationship(user, user2))
    session.commit()

def read_watching(fname):
    username = path.basename(fname)
    username = username[:-len('.watching')]
    date_checked = datetime.fromtimestamp(int(os.stat(fname).st_mtime))
    watching = []
    for line in file(fname):
        line = line.strip()
        if not line:
            continue
        watching.append(line)
    return username, date_checked, watching

def upload_watching(username, date_checked, watching, create_session=None):
    if create_session is None:
        import gitpointer.backend
        create_session = gitpointer.backend.create_session
    session = create_session()
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise ValueError('user is None')
    for w in watching:
        owner, name = owner_name_of(w)
        repo = session.query(Repository) \
                        .filter(Repository.owner == owner) \
                        .filter(Repository.name == name) \
                        .first()
        if repo is None:
            repo = Repository(owner, name, None)
            session.add(repo)
        session.add(WatchRelationship(user, repo))
    session.commit()

def main():
    from glob import glob
    import gitpointer.backend
    create_session = gitpointer.backend.create_session
    session = create_session()
    c = session.connection()
    # This is only valid for SQLite3, but it makes it much faster
    c.execute('''PRAGMA SYNCHRONOUS=OFF;''')
    for fname in glob('database/*/*.follow'):
        upload_user(*read_user(fname), create_session=(lambda : session))
    for fname in glob('database/*/*.watching'):
        upload_watching(*read_watching(fname), create_session=(lambda : session))

if __name__ == '__main__':
    main()

