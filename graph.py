#!/usr/bin/env python

"""
Basic, undirected graph data structure (with weighted edges).

Note: not threadsafe whatsoever.
"""

class Graph(object):
    def __init__(self, vertices, edges):
        """
        Vertices should be a list of strings.
        
        Edges should be a list of (v1, v2, weight) tuples, where v1 and v2
        are names of vertices and weight is a numerical value.
        """
        for a, b, weight in edges:
            assert a in vertices
            assert b in vertices
        
        self.vertices = vertices
        self.edges = edges
    
    def edges_from(self, a):
        "Yields (b, w) vertex-weight pairs."
        for v1, v2, w in self.edges:
            if a == v1:
                yield (v2, w)
            elif a == v2:
                yield (v1, 1.0/w)
    
    def path(self, a, b):
        "Returns a list of edges, (v1, v2, w) connecting a to b."
        # slightly modified Dijkstra's algorithm
        # http://en.wikipedia.org/wiki/Dijkstra's_algorithm
        dist = {}
        prev = {}
        conv = {}
        for v in self.vertices:
            dist[v] = 1e99
            prev[v] = None
            conv[v] = 0
        
        dist[a] = 0
        conv[a] = 1
        Q = list(self.vertices)
        
        found = False
        while Q and not found:
            Q.sort(key=dist.__getitem__)
            u = Q.pop(0)
            if dist[u] == 1e99:
                break
            for v, w in self.edges_from(u):
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    conv[v] = w
                        
        mult = 1.0
        path = [b]
        p = b
        while p != a:
            mult *= conv[p]
            p = prev[p]
            if p is None:
                raise ValueError, "No path exists between %s and %s" % (a, b)
            path.insert(0, p)
        
        return mult, path
    