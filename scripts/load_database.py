import os
from os import path
from gitpointer.models import User, FollowingRelationship
from datetime import datetime

def read_user(fname):
    username = path.basename(fname)
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
        session.add(FollowingRelationship(user.id, user2.id))
    session.commit()
    session.close()

def main():
    from glob import glob
    import gitpointer.backend
    create_session = gitpointer.backend.create_session
    session = create_session()
    c = session.connection()
    # This is only valid for SQLite3, but it makes it much faster
    c.execute('''PRAGMA SYNCHRONOUS=OFF;''')
    for i,fname in enumerate(glob('database/*/*')):
        upload_user(*read_user(fname), create_session=(lambda : session))
        if (i % 1000) == 0: print i

if __name__ == '__main__':
    main()

