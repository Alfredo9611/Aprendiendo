import string
import numpy

from Graph import Vertex, Edge, Graph
from SmallWorldGraph import SmallWorldGraph
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*,cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# IPython Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# dotenv
.env

# virtualenv
venv/
ENV/

# Spyder project settings
.spyderproject

# Rope project settings
.ropeproject
class Vertex(object):
    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__


class Edge(tuple):
    def __new__(cls, *vs):
        if len(vs) != 2:
            raise ValueError ('Edges must connect exactly two vertices.')
        return tuple.__new__(cls, vs)

    def __repr__(self):
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__


class Graph(dict):
    def __init__(self, vs=[], es=[]):
        for v in vs:
            self.add_vertex(v)
            
        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        self[v] = {}

    def add_edge(self, e):
        v, w = e
        self[v][w] = e
        self[w][v] = e

    def get_edge(self, v1, v2):
        try:
            return self[v1][v2]
        except KeyError:
            return None

    def remove_edge(self, e):
        if self.get_edge(e[0], e[1]) != None:
            del self[e[0]][e[1]]
            del self[e[1]][e[0]]
            del e

    def vertices(self):
        return self.keys()

    def edges(self):
        edges = []
        for v in self:
            for w in self[v]:
                if self[v][w] != {} and self[v][w] not in edges:
                    edges.append(self[v][w])
        return edges

    def out_vertices(self, v):
        return self[v].keys()

    def out_edges(self, v):
        edges = []
        for w in self[v]:
            if self[v][w] != {} and self[v][w] not in edges:
                edges.append(self[v][w])
        return edges

    def add_all_edges(self):
        for v in self:
            for w in self:
                if v != w:
                    self.add_edge(Edge(v,w))

    def add_regular_edges(self, k):
        """the necessary and sufficient condition for a k-regular graph of order n to exist
        are that n>=k+1 and that n*k is even"""
        if (len(self.vertices()) <= k or (len(self.vertices())*k) % 2 != 0):
            print ('preconditions not met')
            return

        vs = self.vertices()

        for i in range(len(vs)):
            for j in range(i - (k/2), i + (k/2)-1):
                if (i != j):
                        self.add_edge(Edge(vs[i], vs[j % len(vs)]))

                if (k%2 != 0):
                    self.add_edge(Edge(vs[i], vs[ (i+(len(vs)/2)) % len(vs)]))

    def is_connected(self):
        start = self.vertices()[0]
        queue = []
        marked = []
        queue.append(start)

        while (queue):
            current = queue[0]
            marked.append(current)
            queue.remove(queue[0])

            for w in self.out_vertices(current):
                if w not in marked and w not in queue:
                    queue.append(w)

        if set(marked) == set(self.vertices()):
            print ('Connected!')
            return True
        else:
            print ('Not connected!')
            return False


def main(script, *args):
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e = Edge(v, w)
    d = Edge(v, x)
    
    g = Graph([v,w,x], [e,d])
    print ( g)
    print

    print (g.vertices())

    print( g.edges())

    print (g.out_vertices(v))

    print( g.out_edges(v))

    g.add_all_edges()

    print (g)

if __name__ == '__main__':
    import sys
    main(*sys.argv)

def main(script, n='1000', k='10', *args):

    n = int(n) #number of vertices
    k = int(k) #number of edges in regular graph
    vertices = [Vertex(c) for c in range(n)]

    g = SmallWorldGraph(vertices)
    g.add_regular_edges(k)

    #regular graph's clustering coefficient and avg path length
    c_zero = g.clustering_coefficient()
    l_zero = g.average_path_length()
    print (c_zero, l_zero)

    f = open("plots/output.csv", "wb")
    print ('p\tC\tL')
    f.write('p,C(p)/C(0),L(p)/L(0)\n')

    #begin rewiring to tease out small-world network characteristics
    for log_exp in numpy.arange(-40, 1, 1): #incrementation scheme for logarithmic exponents
        g = SmallWorldGraph(vertices)
        g.add_regular_edges(k)
        p = numpy.power(10, log_exp/10.0)
        g.rewire(p)
        print ('%s\t%s\t%s' % (p, g.clustering_coefficient()/c_zero, g.average_path_length()/l_zero))
        f.write('%s,%s,%s\n' % (p, g.clustering_coefficient()/c_zero, g.average_path_length()/l_zero))
    f.close()


if __name__ == '__main__':
    import sys
    main(*sys.argv)