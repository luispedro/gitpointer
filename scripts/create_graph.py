import tinygraph
from gitpointer.models import User, FollowingRelationship
import gitpointer.backend

TG = tinygraph.TinyGraph()
create_session = gitpointer.backend.create_session
session = create_session()

q = session.query(FollowingRelationship)
for fr in q.yield_per(10):
    TG.add_edge(fr.follower_id, fr.followee_id)
TG.finish()
TG.dump('gitpointer.graph')
