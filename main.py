"""
Run this script to test out each methods. Feel free to tune the parameters.
"""
# ==== VARIABLES ============================================================= #

POPULATION_SIZE = 512
TRAVERSAL_SIZE  = 8

# ==== IMPORTS =============================================================== #

print("Running genetic algorithm...")
import genetic_algo_method as gam

print("Running graph method...")
import graph_method        as gm
print(gm.City(gm.generate_population(POPULATION_SIZE, TRAVERSAL_SIZE)).optimize_gt())

# ==== EOF =================================================================== #