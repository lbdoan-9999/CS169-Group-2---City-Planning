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
    
    GT  = np.genfromtxt('results/gt_results', delimiter = ',')
    GA  = np.genfromtxt('results/ga_results', delimiter = ',')
    #fig = plt.figure()
    #ax  = plt.axes(projection = '3d')
    
    population_size0 = GT[:, 0]
    traversal_size0  = GT[:, 1]
    total_distance0  = GT[:, 2]
    function_calls0  = GT[:, 4]
    runtime_second0  = GT[:, 6]
    population_size1 = GA[:, 0]
    traversal_size1  = GA[:, 1]
    total_distance1  = GA[:, 2]
    function_calls1  = GA[:, 3]
    runtime_second1  = GA[:, 4]
    
    plt.scatter(traversal_size0, runtime_second0, c = 'red')
    plt.scatter(traversal_size1, runtime_second1, c = 'green')
    plt.show()

# ==== MAIN ================================================================== #

def main():
    
    evaluate()


if __name__ == "__main__":
    
    main()