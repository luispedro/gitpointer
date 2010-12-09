import tinygraph
import numpy as np

def baseline(nr_steps=(10*1000*1000), burn_in=1000, initial=1, visited=None):
    if visited is None:
        visited = np.zeros(TG.nr_nodes())
    cur = initial 
    for i in xrange(burn_in):
        cur = TG.random_step(cur)
    for i in xrange(nr_steps):
        visited[cur] += 1
        cur = TG.random_step(cur)
    return visited

def visited_from(TG, start, walks=10000, steps=10):
    visited = np.zeros(TG.nr_nodes())
    for i in xrange(walks):
        cur = start
        for i in xrange(steps):
            cur = TG.random_step(cur)
            visited[cur] += 1
    return visited

def select_best(visited, visited_from):
    ratio = (1./((-.25)*visited - .25) + 5) * visited_from/(1+visited)
    argsorted = ratio.argsort()
    return argsorted[::-1]

if __name__ == '__main__':
    import gitpointer.backend
    from gitpointer.models import User
    TG = tinygraph.TinyGraph()
    TG.load('gitpointer.graph')
    create_session = gitpointer.backend.create_session
    session = create_session()
    stationary = baseline()
    visited_from_239 = visited_from(TG, 239)
    best = select_best(stationary, visited_from_239)
    for i in best[:10]:
        print session.query(User).get(int(i)).username
