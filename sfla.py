#! usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
sns.set_context("notebook")



n_boulders = 150
boulders = np.random.uniform(0., 1., (n_boulders, 3))
boulders[:, 2] = 1 / (3 ** np.random.choice(range(2, 4), (n_boulders)))



def opt_func(f):
    """The mathematical function to optimize.
    Boulder here"""
    x = f[0]
    y = f[1]
    res = 0
    for i in range(boulders.shape[0]):
        eval_ = (
            (x - boulders[i, 0]) ** 2
            + (y - boulders[i, 1]) ** 2
            - boulders[i, 2] ** 2
        )
        if eval_ < 0:
            res += eval_
    return res




def gen_frogs(frogs, dimension):
    """Generates a random frog population from gaussian normal distribution.
    
    Arguments:
        frogs {int} -- Number of frogs
        dimension {int} -- Dimension of frogs/ Number of features
    
    Returns:
        numpy.ndarray -- A frogs x dimension array
    """
    frogs = np.array([[np.random.uniform(0,1) for i in range(dimension)]for j in range(frogs)])
    return frogs



def sort_frogs(frogs, mplx_no, opt_func):
    """Sorts the frogs in decending order of fitness by the given function.
    
    Arguments:
        frogs {numpy.ndarray} -- Frogs to be sorted
        mplx_no {int} -- Number of memeplexes, when divides frog number should return an integer otherwise frogs will be skipped
        opt_func {function} -- Function to determine fitness
    
    Returns:
        numpy.ndarray -- A memeplexes x frogs/memeplexes array of indices, [0, 0] will be the greatest frog
    """

    # Find fitness of each frog
    fitness = np.array(list(map(opt_func, frogs)))
    # Sort the indices in decending order by fitness
    sorted_fitness = np.argsort(fitness)
    # Empty holder for memeplexes
    memeplexes = np.zeros((mplx_no, int(frogs.shape[0]/mplx_no)))
    # Sort into memeplexes
    for j in range(memeplexes.shape[1]):
        for i in range(mplx_no):
            memeplexes[i, j] = sorted_fitness[i+(mplx_no*j)]
    return memeplexes




def local_search(frogs, memeplex, opt_func):
    """Performs the local search for a memeplex.
    
    Arguments:
        frogs {numpy.ndarray} -- All the frogs
        memeplex {numpy.ndarray} -- One memeplex
        opt_func {function} -- The function to optimize
        sigma {int/float} -- Sigma for the gaussian distribution by which the frogs were created
        mu {int/float} -- Mu for the gaussian distribution by which the frogs were created
    
    Returns:
        numpy.ndarray -- The updated frogs, same dimensions
    """

    # Select worst, best, greatest frogs
    frog_w = frogs[int(memeplex[-1])]
    frog_b = frogs[int(memeplex[0])]
    frog_g = frogs[0]
    # Move worst wrt best frog
    frog_w_new = frog_w + (np.random.rand() * (frog_b - frog_w))
    # If change not better, move worst wrt greatest frog
    if opt_func(frog_w_new) > opt_func(frog_w):
        frog_w_new = frog_w + (np.random.rand() * (frog_g - frog_w))
    # If change not better, random new worst frog
    if opt_func(frog_w_new) > opt_func(frog_w):
        frog_w_new = gen_frogs(1, frogs.shape[1])[0]
    # Replace worst frog
    frogs[int(memeplex[-1])] = frog_w_new
    return frogs





def shuffle_memeplexes(frogs, memeplexes):
    """Shuffles the memeplexes without sorting them.
    
    Arguments:
        frogs {numpy.ndarray} -- All the frogs
        memeplexes {numpy.ndarray} -- The memeplexes
    
    Returns:
        numpy.ndarray -- A shuffled memeplex, unsorted, same dimensions
    """

    # Flatten the array
    temp = memeplexes.flatten()
    #Shuffle the array
    np.random.shuffle(temp)
    # Reshape
    temp = temp.reshape((memeplexes.shape[0], memeplexes.shape[1]))
    return temp




def sfla(opt_func, frogs=30, dimension=2, mplx_no=5, mplx_iters=10, solun_iters=50):
    """Performs the Shuffled Leaping Frog Algorithm.
    
    Arguments:
        opt_func {function} -- The function to optimize.
    
    Keyword Arguments:
        frogs {int} -- The number of frogs to use (default: {30})
        dimension {int} -- The dimension/number of features (default: {2})
        mplx_no {int} -- Number of memeplexes, when divides frog number should return an integer otherwise frogs will be skipped (default: {5})
        mplx_iters {int} -- Number of times a single memeplex will be iterated before shuffling (default: {10})
        solun_iters {int} -- Number of times the memeplexes will be shuffled (default: {50})
    
    Returns:
        tuple(numpy.ndarray, numpy.ndarray, numpy.ndarray) -- [description]
    """
    # Generate frogs around the solution
    frogs = gen_frogs(frogs, dimension)
    # Arrange frogs and sort into memeplexes
    memeplexes = sort_frogs(frogs, mplx_no, opt_func)
    # Best solution as greatest frog
    best_solun = frogs[int(memeplexes[0, 0])]
    # For the number of iterations
    for i in range(solun_iters):
        # Shuffle memeplexes
        memeplexes = shuffle_memeplexes(frogs, memeplexes)
        # For each memeplex
        for mplx_idx, memeplex in enumerate(memeplexes):
            # For number of memeplex iterations
            for j in range(mplx_iters):
                # Perform local search
                frogs = local_search(frogs, memeplex, opt_func)
            # Rearrange memeplexes
            memeplexes = sort_frogs(frogs, mplx_no, opt_func)
            # Check and select new best frog as the greatest frog
            new_best_solun = frogs[int(memeplexes[0, 0])]
            if opt_func(new_best_solun) < opt_func(best_solun):
                best_solun = new_best_solun
    return best_solun, frogs, memeplexes.astype(int)




def sfla_iter(opt_func,X,Y,Z, frogs=80, dimension=2,  mplx_no=5, mplx_iters=10, solun_iters=50):
    """Performs the Shuffled Leaping Frog Algorithm.
    Every twenty iterations, we print the funtion to optimize and the positions of the memeplexes, in order to vizualize the progressions
    
    Arguments:
        opt_func {function} -- The function to optimize.
    
    Keyword Arguments:
        frogs {int} -- The number of frogs to use (default: {30})
        dimension {int} -- The dimension/number of features (default: {2})
        mplx_no {int} -- Number of memeplexes, when divides frog number should return an integer otherwise frogs will be skipped (default: {5})
        mplx_iters {int} -- Number of times a single memeplex will be iterated before shuffling (default: {10})
        solun_iters {int} -- Number of times the memeplexes will be shuffled (default: {50})
    
    Returns:
        tuple(numpy.ndarray, numpy.ndarray, numpy.ndarray) -- [description]
    """

    # Generate frogs around the solution
    frogs = gen_frogs(frogs, dimension)
    # Arrange frogs and sort into memeplexes
    
    memeplexes = sort_frogs(frogs, mplx_no, opt_func)
    # Best solution as greatest frog
    best_solun = frogs[int(memeplexes[0, 0])]
    # For the number of iterations
    for i in range(solun_iters):
        # Shuffle memeplexes
        memeplexes = shuffle_memeplexes(frogs, memeplexes)
        # For each memeplex
        for mplx_idx, memeplex in enumerate(memeplexes):
            # For number of memeplex iterations
            for j in range(mplx_iters):
                # Perform local search
                frogs = local_search(frogs, memeplex, opt_func)
            # Rearrange memeplexes
            memeplexes = sort_frogs(frogs, mplx_no, opt_func)
            # Check and select new best frog as the greatest frog
            new_best_solun = frogs[int(memeplexes[0, 0])]
            if opt_func(new_best_solun) < opt_func(best_solun):
                best_solun = new_best_solun
                
                
        if(i%20==0 or i == solun_iters-1):
            print("Optimal Solution for ",i, " iterations : {}".format(best_solun))
    
            # Place memeplexes
            plt.figure()
            for idx, memeplex in enumerate(memeplexes):
                memeplex = np.array(memeplex).astype(int)
                plt.scatter(frogs[memeplex, 0], frogs[memeplex, 1], marker='x', label="memeplex {}".format(idx))
            plt.scatter(best_solun[0], best_solun[1], marker='o', label="Optimal Solution")
            #plt.scatter(0, 0, marker='*', label='Actual Solution')
            # Plot properties
            #if(i == 0):
            #    plt.legend()
            plt.xlabel("x-axis")
            plt.ylabel("y-axis")
            plt.title("Shuffled Frogs")
            plt.contour(X, Y, Z, alpha=.5)
            # Show plot
            plt.show()
    return best_solun, frogs, memeplexes.astype(int)




def main():
    # Run algorithm
    solun, frogs, memeplexes = sfla(opt_func, 100, 2, 10, 0, 5, 25, 400)
    print("Optimal Solution (closest to zero): {}".format(solun))
    # Place memeplexes
    for idx, memeplex in enumerate(memeplexes):
        plt.scatter(frogs[memeplex, 0], frogs[memeplex, 1], marker='x', label="memeplex {}".format(idx))
    plt.scatter(solun[0], solun[1], marker='o', label="Optimal Solution")
    plt.scatter(0, 0, marker='*', label='Actual Solution')
    # Plot properties
    plt.legend()
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Shuffled Frogs")
    # Show plot
    plt.show()

if __name__ == '__main__':
    main()
