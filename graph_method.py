# ==== IMPORT ================================================================ #

from itertools import combinations, groupby, product
from time      import time

import math
import random as rand

# ==== CACHE ================================================================= #

CACHE_SIZE = 32
DIST_CACHE = [[[[(abs(y - w) + abs(z - x)) for z in range(-CACHE_SIZE, CACHE_SIZE)] \
                                           for y in range(-CACHE_SIZE, CACHE_SIZE)] \
                                           for x in range(-CACHE_SIZE, CACHE_SIZE)] \
                                           for w in range(-CACHE_SIZE, CACHE_SIZE)]

# ==== HELPER FUNCTIONS ====================================================== #

def most_common_edges(loc, ajm):
    
    """
    Return a list of edges with the most recurrence.
    |
    loc := {str}           set of edges to evaluate for
    ajm := {str:{str:int}} adjacency matrix of edge recurrence
    """
    
    m = -1
    
    for (x, y) in combinations(loc, 2):
        
        if ajm[x][y] > m:
            
            l = [{x, y}]
            m = ajm[x][y]
        
        elif ajm[x][y] == m:
            
            l.append({x, y})
    
    return [loc] if len(loc) == 1 else l


def count_common_vertices(edges):
    
    """
    Return a dictionary with key of vertices occurence and value of said
    vertices.
    |
    edges := [{str}] list of edges to evaluate for
    """
    
    d = {}
    l = [vertex for edge in edges for vertex in edge]
    
    for vertex in set(l):
        
        cnt = l.count(vertex)
        
        if cnt not in d: d[cnt] = {vertex}
        else:            d[cnt].add(vertex)
    
    return d


def generate_location(t, n):
    
    """
    Generate locations based on type.
    t = 0: residential
    t = 1: commercial
    t = 2: residential + commercial
    |
    t := (uint) area type
    n := (uint) population size
    """
    
    if t == 0:
        
        l = ["Home "      + str(i) for i in range(n >> 2)] + \
            ["Apartment " + str(i) for i in range(n >> 6)]
    
    else:
        
        l = ["Home "      + str(i) for i in range(n >> 2)]      + \
            ["Apartment " + str(i) for i in range(n >> 6)]      + \
            ["Store "          + str(i) for i in range(n >> 6)] + \
            ["Gym "            + str(i) for i in range(n >> 8)] + \
            ["School "         + str(i) for i in range(n >> 8)] + \
            ["Library "        + str(i) for i in range(n >> 8)] + \
            ["Gas Station "    + str(i) for i in range(n >> 6)] + \
            ["Studio "         + str(i) for i in range(n >> 9)] + \
            ["Amusement Park " + str(i) for i in range(n >> 9)] + \
            ["Park "           + str(i) for i in range(n >> 8)] + \
            ["Theatre "        + str(i) for i in range(n >> 8)] + \
            ["Car Dealer "     + str(i) for i in range(n >> 8)] + \
            ["University "     + str(i) for i in range(n >> 9)] + \
            ["Mall "           + str(i) for i in range(n >> 9)]
    
    return l


def generate_resident(n, res, mix):
    
    """
    Generate a sequence of size n of vertices that represent the walk of some
    arbitrary resident in the city.
    |
    n   := (uint) the number of vertices in the walk
    res := [str] list of residential areas
    mix := [str] list of residential and commercial areas
    """
    
    l = [rand.choice(res)] + rand.choices(mix, k = 1 if n < 1 else n)
    
    return [v[0] for v in groupby(l)] + [l[0]]


def generate_population(n, μ, σ = 1):
    
    """
    Generate a set of size n of residents in a population with a traversal size
    generated from a Gaussian distribution with mean μ and standard deviation σ.
    |
    n := (uint) population size
    μ := (uint) mean of traversal size
    σ := (uint) standard deviation of traversal size
    """
    
    r = generate_location(0, n)
    m = generate_location(1, n)
    
    return [generate_resident(round(rand.gauss(μ, σ)), r, m) for _ in range(n)]

# ==== CLASSES =============================================================== #

class City():
    
    """
    Just a wrapper class. Provide some helpful properties and or methods for
    optimization methods.
    """
    
    def __init__(self, pop):
        
        """
        pop := [[str]] lists of traversals
        """
        
        self.loc = set([vertex for res in pop for vertex in res])
        self.map = Map(len(self.loc))
        
        # ==== Generate an adjacency-matrix. ==== #
        
        self.ajm = {x:{y:0 for y in self.loc} for x in self.loc}
        
        for res in pop:
            
            for i in range(len(res) - 1):
                
                self.ajm[res[i]][res[i + 1]] += 1
                self.ajm[res[i + 1]][res[i]] += 1
        
        # ==== END ============================== #
    
    
    def copy(self):
        
        """
        Return a copy of City.
        """
        
        tmp     = City([[]])
        tmp.ajm = dict(self.ajm)
        tmp.loc = set(self.loc)
        tmp.map = self.map.copy()
        
        return tmp
    
    
    def test_dist(self, a, vertices, m):
        
        d = 0
        
        for b in vertices:
            
            if self.ajm[a][b]:
                
                d += self.ajm[a][b] * DIST_CACHE[m.place[a].x + CACHE_SIZE][m.place[a].y + CACHE_SIZE][m.place[b].x + CACHE_SIZE][m.place[b].y + CACHE_SIZE]
        
        return d
    
    
    def test_tot_dist(self, vertices, m):
        
        """
        Compute total distance of currently placed locations.
        |
        vertices := [str] list of locations to measure distance
        m        := (Map) map to evaluate for
        """
        
        d = 0
        
        for (a, b) in combinations(vertices, 2):
            
            if self.ajm[a][b]:
                
                d += self.ajm[a][b] * DIST_CACHE[m.place[a].x + CACHE_SIZE][m.place[a].y + CACHE_SIZE][m.place[b].x + CACHE_SIZE][m.place[b].y + CACHE_SIZE]
                
        
        return d
    
    
    def optimize_gt(self):
        
        """
        Optimize via graph theory.
        """
        
        T = time()
        n = 0
        
        loc_tmp = set(self.loc)
        map_tmp = self.map.copy()
        fixed   = set()
        
        while loc_tmp:
            
            # Generate common vertices of the most common edges.
            cvmce = count_common_vertices(most_common_edges(loc_tmp, self.ajm))
            
            for cnt in sorted(cvmce.keys(), reverse = True):
                
                while cvmce[cnt]:
                
                    min_dist = math.inf
                    
                    for (P, name) in product(map_tmp.border(), cvmce[cnt]):
                        
                        n += 1
                        
                        # Temporary insert locations at coordinate for evaluation.
                        map_tmp.insert(P.x, P.y, name)
                        
                        # Evaluate possible placement.
                        
                        # Room for optimization. Just evaluate the newly added
                        # point for the map_tmp.
                        dist_tmp = self.test_dist(name, fixed, map_tmp)
                        
                        if dist_tmp < min_dist:
                        
                            min_dist = dist_tmp
                            opt_P    = P
                            opt_name = name
                        
                        # Revert change.
                        map_tmp.undo()
                    
                    # Add permanent update to solution.
                    map_tmp.insert(opt_P.x, opt_P.y, opt_name)
                    fixed.add(opt_name)
                    cvmce[cnt].remove(opt_name)
                    loc_tmp.remove(opt_name)
        
        return (self.test_tot_dist(fixed, map_tmp), n, time() - T)
    
    
    def optimize_na(self):
        
        pass
    
    """
    def random_placement(self):
        
        loc_tmp = list(self.loc)
        map_tmp = Map(len(self.loc))
        
        while loc_tmp:
            
            t = tuple(map_tmp.border())
            p = rand.choice(t)
            l = rand.choice(loc_tmp)
                
            map_tmp.insert(p.x, p.y, l)
            loc_tmp.remove(l)
        
        return self.test_tot_dist(self.loc, map_tmp)
    """

class Map():
    
    def __init__(self, n):
        
        """
        n := (uint) size of plane [-n, n)
        """
        
        self.hist  = {}
        self.place = {}
        self.plane = {x:{y:0 for y in range(-n, n)} for x in range(-n, n)}
        self.point = {Pair(0, 0)}
        self.size  = n
    
    
    def border(self):
        
        """
        Return a copy of the border points.
        """
        
        return set(self.point)
    
    
    def copy(self):
        
        """
        Return a copy of Map.
        """
        
        tmp       = Map(self.size)
        tmp.place = dict(self.place)
        tmp.plane = dict(self.plane)
        tmp.point = set(self.point)
        
        return tmp
    
    
    def insert(self, x, y, name, err = 1):
        
        """
        Insert a point to self.plane and map them to self.place. Add in new
        borders.
        |
        x    := (int)  x-value
        y    := (int)  y-value
        name := (str)  name of location
        warn := (bool) prohibit inserting coordinate not at the border
        """
        
        if Pair(x, y) in self.point or not err:
            
            # Clear history for update.
            self.hist          = {}
            self.hist["place"] = name
            self.hist["plane"] = []
            
            self.place[name] = Pair(x, y)
            self.plane[x][y] = 1
            
            self.point.remove(Pair(x, y))
            
            for (a, b) in ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)):
                
                if Pair(a, b) not in self.point and not self.plane[a][b]:
                    
                    self.point.add(Pair(a, b))
                    self.hist["plane"].append(Pair(a, b))
        
        else:
            
            print("ERROR: (%d, %d) is not on the border." %(x, y))
    
    
    def undo(self):
        
        """
        Undo previous transaction.
        """
        
        # Undo added border points.
        for v in self.hist["plane"]: self.point.remove(v)
        
        # Undo added location.
        v = self.place.pop(self.hist["place"])
        
        # Undo allocated point.
        self.plane[v.x][v.y] = 0
        
        # Undo removed point.
        self.point.add(v)
        
        self.hist = {}


class Pair():
    
    def __init__(self, x, y):
        
        """
        x := (int) x-value
        y := (int) y-value
        """
        
        self.x = x
        self.y = y
    
    
    def __eq__(self, X):
        
        return self.x == X.x and self.y == X.y
    
    
    def __hash__(self):
        
        return (self.x, self.y).__hash__()
    
    
    def __repr__(self):
        
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    
    def __str__(self):
        
        return self.__repr__()
    
    
    def copy(self):
        
        """
        Return a copy of Pair.
        """
        
        return Pair(self.x, self.y)
    
    
    def dist(self, X):
        
        """
        Return taxicab geometry distance.
        |
        X := (Pair) point to evaluate to
        """
        
        return abs(self.x - X.x) + abs(self.y - X.y)

# ==== EOF =================================================================== #
if __name__ == "__main__":
    A = City(generate_population(1024, 10))
    print(A.optimize_gt())
    print(A.random_placement())
