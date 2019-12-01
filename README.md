# SFLA
Metaheuristics:  Shuffled Leaping Frog Algorithme (SFLA)


- Using https://github.com/theDIG95/Shuffled-frog-leaping-algorithm as a base code
- Adapted in order to minimize boulders functions.



#### Description and Definitions: 

An optimization algorithm derived from observing the movement of frogs while they search from a food source:

- Frogs are divided into groups (named memeplexes) and take advantage from the knowledge of other groups. 
- Inside each memeplexe, the worst frog tries to improve its position, which improves the overall group and ultimately the colony.


This algorithm will be used to optimize a n-dimensional boulders function. In order to plot the results, we will here show how to use it for 2-dimensional data. To see how boulders functions they are generated, check sfla.py.

The fitness is the opposite of the boulders function (the lower the function is, the highest the fitness is). 





## Algorithm

#### 1. Frog population sorting and division


- Randomly initialize n frogs to use (here using np.random.uniform()). 
- Then these frogs are divided into m number of memeplexes. 


The global population of frogs is sorted using the descending order of fitness, so that the top fitness frogs are in different memeplexes. For example if there are 2 memeplexes, then the highest fitness frog is in memeplex 1, the 2nd fittest frog is in memeplex 2, 3rd fittest frog is again in memeplex 1 and so on.




#### 2. Local search per memeplex

1 - Inside each memeplexe, move the frog having the worst fitness towards the frog having the best one


2 - If its fitness has not improved: Move the worst frog toward the greatest frog of the overall population


3 - If its fitness has not improved: Set the frog to a new randomly selected position


#### 3. Shuffle the memeplexes
We shuffle the memeplexes after the local search so that some frogs are redistributed among other memplexes, in order to improve each one of them based on the knowledge of the others.


#### 4. Termination

Different thresholds can be used as a terminating condition. Here, a maximum number of iteration is used. We could also use other criteria such as if the frog with the best fitness doesn't  significantly improve its fitness over a few loops.
