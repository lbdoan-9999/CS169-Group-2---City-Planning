# ==== IMPORT ================================================================ #

from itertools       import product
from multiprocessing import Pool
from statistics      import mean, stdev

import graph_method      as gm
import matplotlib.pyplot as plt
import numpy             as np

# ==== FUNCTIONS ============================================================= #

def benchmark(s):
    
    p = (4, 5, 6, 7, 8)
    
    for n in p:
        
        dist = []
        call = []
        time = []
        
        for i in range(128):
            
            r = gm.City(gm.generate_population(s, n)).optimize_gt()
            dist.append(r[0])
            call.append(r[1])
            time.append(r[2])
            
        f = open("results/gt_results", "a")
        f.write(str(s) + "," + str(n) + "," + \
                str(mean(dist)) + "," + str(stdev(dist)) + "," + \
                str(mean(call)) + "," + str(stdev(call)) + "," + \
                str(mean(time)) + "," + str(stdev(time)) + "\n")
        
        f.close()
    
    print("Done with size " + str(s))


def mt_benchmark():
    
    p = Pool()
    o = p.map(benchmark, (s for s in range(16, 1025)))
    p.close()
    p.join()


def evaluate():
    
    D   = np.genfromtxt('results/gt_results', delimiter = ',')
    fig = plt.figure()
    ax  = plt.axes(projection = '3d')
    
    population_size = D[:, 0]
    traversal_size  = D[:, 1]
    total_distance  = D[:, 2]
    function_calls  = D[:, 4]
    runtime_second  = D[:, 6]
    
    ax.scatter(population_size, traversal_size, runtime_second, c = total_distance, cmap = 'viridis')
    plt.show()

# ==== MAIN ================================================================== #

def main():
    
    evaluate()


if __name__ == "__main__":
    
    main()