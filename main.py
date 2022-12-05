"""
Run this script to test out each methods. Feel free to tune the parameters.
"""
# ==== VARIABLES ============================================================= #

POPULATION_SIZE = 512
TRAVERSAL_SIZE  = 8

# ==== IMPORTS =============================================================== #

print("Running genetic algorithm...")
import genetic_algo_method as ga


adjList = ga.generate_population(512, 8)

# get smallest m and n possible to fit k unique locations in a grid
m, n = ga.generate_dimensions(len(adjList.array))

k_max = 5*len(adjList.array)
population = ga.rand_population(adjList, m, n, int(k_max*.2))

S = ga.TournamentSelection(int(k_max*.1))

x, time = ga.genetic_algorithm(ga.f, population, k_max, S, adjList)

print("(" + str(ga.f(x, adjList)) + ", " + str(k_max) + ", " + str(time) + ")")


print("Running graph method...")
import graph_method        as gm
print(gm.City(gm.generate_population(POPULATION_SIZE, TRAVERSAL_SIZE)).optimize_gt())

# ==== EOF =================================================================== #