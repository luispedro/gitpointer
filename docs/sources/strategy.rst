=======================
Github Suggest Overview
=======================

Github suggest was initially a way to test out some graph technology on a
small, but realistic, test graph.

By mining github using its public API, we constructed a two-colour graph where
nodes are either users or repositories and a link exists between:

- users following each other
- users watching a repository
- a repository and its owner

We interpreted this as an undirected graph.

A random walk in this graph, starts at some node and, at each step, randomly
chooses one of its neighbours to hop to (the choice is uniform: all neighbours
are equally likely).

If a random walk goes on long enough (technically, as it approaches an infinite
number of steps), each node will show up with some probability $p(n)$. This is
the *stationary probability* of the random walk. More "central" nodes have
higher $p(n)$ values and this measure is interesting in and of itself.

There are several ways to approximate this distribution. Given that the graph
is relatively small, we chose to simply simulate a few long random walks. On a
laptop, with the inner loop running in Python (but using our optimised graph
representation in C++), it takes 106s to perform 10 million steps.

For recommending possible users or repositories, github suggest performs a
series of small (10 step) random walks starting at the user of interest. Those
nodes with a higher than expected visitation rate are recommended.

This straightforward approach was fragile to nodes which had a very small
stationary probability (and which could therefore easily be over-represented in
the random walks starting from the node of interest, even if they are not very
relevant). Therefore, we introduce a correction such that a node with less than
4 incoming connections is weighted down.

