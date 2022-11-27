# ==== IMPORT ================================================================ #

from itertools       import product
from multiprocessing import Pool

import graph_method as gm

# ==== FUNCTIONS ============================================================= #

def benchmark(s):
    
    p = (256, 512, 768, 1024)
    
    for n in p:
        
        for i in range(16):
            
            f = open("results/gt_" + str(n) + "_" + str(s), "a")
            r = gm.City(gm.generate_population(n, s)).optimize_gt()
            f.write(str(r[0]) + "," + str(r[1]) + "," + str(r[2]) + "\n")
            f.close()
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