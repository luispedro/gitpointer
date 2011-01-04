import tinygraph
import numpy as np

def baseline(TG, nr_steps=(10*1000*1000), burn_in=1000, initial=1, visited=None):
    '''
    visited = baseline(TG, nr_steps=10M, burn_in=1k, initial=1, visited={np.zeros(TG.nr_nodes())})

    Perform a random walk on `TG`

    Parameters
    ----------
    TG : tinygraph
    nr_steps : integer, optional
        Nr of steps to perform (default: 10M)
    burn_in : integer, optional
        Before starting to record the walk, the function performs some
        unrecorded steps (the "burn in"). This defines how many steps (default:
        1k).
    initial : integer, optional
        Node to start on, (default 1)
    visited : ndarray of size ``TG.nr_nodes()``
        Array to record results in. By default, a new one is allocated.

    Returns
    -------
    visited : ndarray of size ``TG.nr_nodes()``
    '''
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
    '''
    visited = visited_from(TG, start, walks={10k}, steps=10)

    Perform `walks` random walks in `TG`, starting from `start` and taking
    `steps` per walk

    Parameters
    ---------
    TG : tinygraph
    start : integer
        Node in `TG`
    walks : integer, optional
        Nr of random walks to perform (default: 10k)
    steps : integer, optional
        Nr of steps per walk (default: 10)

    Returns
    -------
    visited : ndarray of size ``TG.nr_nodes()``
    '''
    visited = np.zeros(TG.nr_nodes())
    for i in xrange(walks):
        cur = start
        for i in xrange(steps):
            cur = TG.random_step(cur)
            visited[cur] += 1
    return visited

def select_best(baseline_counts, visited_from):
    '''
    best = select_best(baseline_counts, visited_from)

    Parameters
    ----------
    baseline_counts : ndarray
        ndarray of counts in the format returned from `baseline`
    visited_from : ndarray
        ndarray of counts in format return from `visited_from`

    Returns
    -------
    best : ndarray of integers
        Sorted array of integer (node references) such that ``best[0]`` is the
        best recommendation, ``best[1]``, the second best, ...
    '''
    ratio = (1./((-.25)*baseline_counts - .25) + 5) * visited_from/(1+baseline_counts)
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
