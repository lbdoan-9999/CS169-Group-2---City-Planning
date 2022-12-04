# ==== IMPORT ================================================================ #

from itertools       import product
from multiprocessing import Pool

import genetic_algo_method as ga
from graph_method import generate_population

# ==== FUNCTIONS ============================================================= #

def benchmark(s):
    p = (256, 512, 768, 1024)
    
    for n in p:
        for i in range(16):
            
            file = open("results/ga_" + str(n) + "_" + str(s), "a")

            adjList = ga.generate_population(n, s)

            # get smallest a and b possible to fit k unique locations in a grid
            a, b = ga.generate_dimensions(len(adjList.array))

            k_max = 5*len(adjList.array)
            population = ga.rand_population(adjList, a, b, k_max//50)
            
            S = ga.TournamentSelection(k_max//100)

            x, t = ga.genetic_algorithm(ga.f, population, k_max, S, adjList)

            file.write(str(ga.f(x, adjList)) + "," + str(k_max) + "," + str(t) + "\n")
            file.close()
            print("Done with " + str(n) + "_" + str(s) + " #" + str(i))

def mt_benchmark():
    p = Pool(4)
    o = p.map(benchmark, (4, 6, 8, 10))
    p.close()
    p.join()

# ==== MAIN ================================================================== #

def main():
    mt_benchmark()



if __name__ == "__main__":
    
    main()