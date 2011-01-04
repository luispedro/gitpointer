import tinygraph
from gitpointer.models import User, FollowingRelationship, WatchRelationship
import gitpointer.backend

TG = tinygraph.TinyGraph()
create_session = gitpointer.backend.create_session
session = create_session()

q = session.query(FollowingRelationship)
for fr in q.yield_per(10):
    TG.add_edge(fr.follower_id, fr.followee_id)
nusers = session.query(User).count()
q = session.query(WatchRelationship)
for wr in q.yield_per(10):
    if wr.watched_repo is not None:
        TG.add_edge(wr.watcher, wr.watched_repo+nusers)
TG.finish()
TG.dump('gitpointer.graph')
