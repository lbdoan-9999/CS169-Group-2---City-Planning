import random
import copy

from graph_method import generate_location
from time import time

# Selection Method
class TournamentSelection:
    def __init__(self, k):
        self.k = k

class AdjacencyList:
    def __init__(self):
        """
            self.array is a list of pairs where index 0 of a pair is the edge name and 
            index 1 is a list of vertices representing edges
        """
        self.array = []
        
    def add(self, vertexName1, vertexName2):
        vertexFound1 = False
        vertexFound2 = False
        
        for i in range(len(self.array)):
            if self.array[i][0] == vertexName1:
                vertexFound1 = True
                
                # check if edge already exists
                edgeFound = False
                for j in range(len(self.array[i][1])):
                    if self.array[i][1][j] == vertexName2:
                        edgeFound = True
                if not edgeFound:
                    self.array[i][1].append(vertexName2)
                
            elif self.array[i][0] == vertexName2:
                vertexFound2 = True
        
        if not vertexFound1:
            self.array.append([vertexName1,[vertexName2]])
            
        if not vertexFound2:
            self.array.append([vertexName2,[]])
    
    def __len__(self):
        return len(self.array)


def matrixShuffle(matrix):
    # turn it into one big array
    matrixArray = []
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrixArray.append(matrix[i][j])

    # shuffle it
    random.shuffle(matrixArray)
    
    newMatrix = []
    for i in range(0, len(matrixArray), len(matrix[0])):
        newMatrix.append( matrixArray[i : i+len(matrix[0])] )
            
    return newMatrix

""" 
    Creates num randomly shuffled mxn matrices where the indices of the adjacency list
    are put in cells and the remaining cells are -1s
"""
def rand_population(adjList, m, n, num):
    matrices = []
    
    # Create num matrices
    for _ in range(num):
        matrix = []
        j = 0 # keep track of index in adjList
        
        for i in range(m):
            matrix.append([])
            for _ in range(n):
                if j < len(adjList):
                    matrix[i].append(j)
                    j += 1
                else:
                    matrix[i].append(-1)

        # randomly shuffle
        matrices.append(copy.deepcopy(matrixShuffle(matrix)))
    
    return matrices

"""
    Tournament Selection Method from K&W CH9
    t: TournamentSelection
    y: list of f function values
    returns: index for the minimum value of y from t.k randomly chosen indicies 
"""
def getparent(t: TournamentSelection, y):
    # Make an array of randomly shuffled indicies
    p = [ i for i in range(len(y)) ]
    random.shuffle(p)
    
    # select the minimum argument of the first t.k values in p
    minVal = 99999999
    minArg = 0
    for i in p[0:t.k]:
        if minVal > y[i]:
            minVal = y[i]
            minArg = i
    
    return minArg
# y: list of f function values
def select(t: TournamentSelection, y):
    return [[getparent(t,y), getparent(t,y)] for i in y]
    

"""
    Crossover Method inspired by the Uniform Crossover Method in K&W CH9
    a: a parent matrix
    b: a parent matrix
    n: number of unique locations
"""
def crossover(a, b, n):
    # initialize matrix of the same size as a & b with -1's
    child = []
    for row in a:
        newRow = []
        for _ in row:
            newRow.append(-1)
        child.append(newRow)
        
     # find all the indicies in a & b
    indicies = []
    for _ in range(n):
        indicies.append([])
    
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] != -1:
                indicies[a[i][j]].append([i, j])
            if b[i][j] != -1:
                indicies[b[i][j]].append([i, j])
    
    # just in case both random spots are taken 
    replaces = []
    
    # iterate through indicies and randomly choose each cell
    for k in range(len(indicies)):
        # randomly choose 0 or 1
        randIndex = random.randrange(0,2)
        
        i = indicies[k][randIndex][0]
        j = indicies[k][randIndex][1]
        
        # check if cell is already taken
        if child[i][j] != -1:
            # if so we choose the other parent's location
            i = indicies[k][1-randIndex][0]
            j = indicies[k][1-randIndex][1]
            if child[i][j] != -1:
                replaces.append(k)
                continue
            
        child[i][j] = k
    
    x = 0
    stop = False
    
    for i in range(len(child)):
        if stop:
            break
        for j in range(len(child[i])):
            if x >= len(replaces):
                stop = True
                break
            if child[i][j] == -1:
                child[i][j] = replaces[x]
                x += 1
    
    return child
 

"""
    Mutation Method
    child: a child matrix
    n: number of unique locations
"""
def mutate(child, n):
    newChild = matrixShuffle(copy.deepcopy(child))
    return crossover(child, newChild, n)


"""
    Genetic Algorithm optimization method K&W CH9
    f: objective function
    population: initial population
    k_max: number of iterations
    S: a SelectionMethod
    adjList: an adjacency list
"""
def genetic_algorithm(f, population, k_max, S, adjList):
    T = time()
    
    for k in range(k_max):
        parents = select(S, [f(pop, adjList) for pop in population])
        children = [crossover(population[p[0]], population[p[1]], len(adjList))
                    for p in parents]
        population = [mutate(child, len(adjList)) for child in children]
        
    # Select the min arg from
    minVal = 999999999
    minArg = 0
    
    y = [f(pop, adjList) for pop in population]
    
    for i in range(len(y)):
        if minVal > y[i]:
            minVal = y[i]
            minArg = i
    
    return population[minArg], time()-T
    

def create_info_dict(x, adjList):
    infoDict = {}
    
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] != -1:
                infoDict[adjList.array[x[i][j]][0]] = [i, j, x[i][j]]
            
    return infoDict
    
"""
    x: a matrix
    returns: a value
"""
def f(x, adjList):
    sumNum = 0
    
    # Create a dict where the key is the name and the value is a list storing coords
    # and index in adjList so we can calc distances easily
    
    infoDict = create_info_dict(x, adjList)
    
    for key, val in infoDict.items():
        for name in adjList.array[val[2]][1]:
            sumNum += abs(val[0]-infoDict[name][0]) + abs(val[1]-infoDict[name][1])
            
    return sumNum


def generate_resident(n, res, mix, adjList):
    
    """
    Add to an adjacency list using a sequence of size n of vertices
    that represent the walk of some arbitrary resident in the city.
    |
    n   := (uint) the number of vertices in the walk
    res := [str] list of residential areas
    mix := [str] list of residential and commercial areas
    """
    
    home = random.choice(res)

    route = [home] + random.choices(mix, k = 1 if n < 1 else n) + [home]

    for i in range(len(route)-1):
        adjList.add(route[i], route[i+1])

def generate_population(n, μ, σ = 1):
    
    """
    Generate an adjacency list of size n of residents in a population with a traversal size
    generated from a Gaussian distribution with mean μ and standard deviation σ.
    |
    n := (uint) population size
    μ := (uint) mean of traversal size
    σ := (uint) standard deviation of traversal size
    """
    
    r = generate_location(0, n)
    m = generate_location(1, n)

    adjList = AdjacencyList()

    for _ in range(n):
        generate_resident(round(random.gauss(μ, σ)), r, m, adjList)

    return adjList
"""
    Generate optimal dimensions for a grid according to the number of unique locations.
    size: number of unique locations
"""
def generate_dimensions(size):
    m = 10
    n = 10

    # alternate which dimension you are making bigger/smaller
    mTurn = True

    # make it smaller
    while m*n > size:
        if mTurn:
            m -= 1
            mTurn = False
        else:
            n -= 1
            mTurn = True

    # make it bigger
    while m*n < size:
        if mTurn:
            m += 1
            mTurn = False
        else:
            n += 1
            mTurn = True
    
    return m, n

if __name__ == "__main__":

    adjList = generate_population(256, 4)

    # get smallest m and n possible to fit k unique locations in a grid
    m, n = generate_dimensions(len(adjList.array))
    
    population = rand_population(adjList, m, n, 10)
    k_max = 500
    S = TournamentSelection(5)

    x = genetic_algorithm(f, population, k_max, S, adjList)[0]

    print(f(x, adjList))

    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] != -1:
                x[i][j] = adjList.array[x[i][j]][0]

    for row in x:
        print(row)

    """
    adjList = AdjacencyList()
    adjList.add("Home A", "Gym")
    adjList.add("Home A", "Work")
    adjList.add("Home B", "School")
    adjList.add("Apartment", "School")
    adjList.add("Gym", "Library")
    adjList.add("Gym", "Home A")
    adjList.add("School", "Store")
    adjList.add("School", "Gym")
    adjList.add("Library", "Home A")
    adjList.add("Store", "Theater")
    adjList.add("Theater", "Car Dealer")
    adjList.add("Car Dealer", "Home B")
    adjList.add("Work", "Apartment")



    population = rand_population(adjList, 4, 4, 5)
    k_max = 1000
    S = TournamentSelection(500)

    x = genetic_algorithm(f, population, k_max, S, adjList)[0]

    print(f(x, adjList))

    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] != -1:
                x[i][j] = adjList.array[x[i][j]][0]

    for row in x:
        print(row)
    """

