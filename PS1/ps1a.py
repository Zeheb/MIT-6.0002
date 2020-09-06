###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    name_wt_pairs=dict()                                                        # dictionary to return
    fh = open(filename)                                                         # open filehandle

    for line in fh:                                                             # read through file         
        line=line.strip().split(',')                                            # remove spaces and create array of name,wt pair
        name_wt_pairs[line[0]]=int(line[1])                                     # add name,wt pair to dictionary
        
    return name_wt_pairs

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    algo=[]                                                                     # create list to return
    cows_that_left=[]                                                           # to check if the next best cow is gone already
    
    while len(cows_that_left)<len(cows.keys()):                                 # stop when all cows are gone
        curr_wt=0
        curr_trip=[]
        for i in sorted(cows.items(), key=lambda x:x[1], reverse=True):         # sort the dictionary into key,value pairs by weight in ascending order
            if i[1]+curr_wt<=limit and i[0] not in cows_that_left:              # check 1.Weight is acceptable and 2.Cow is on Earth
                curr_trip.append(i[0])                                          # add next best cow to current trip
                curr_wt+=i[1]                                                   # update weight
                cows_that_left.append(i[0])
        algo.append(curr_trip)                                                  # add trip to collection of all trips            
    
    return algo

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    possible_algos=[]                                                          # list containaing acceptable algorithms
    
    for partition in get_partitions(cows):                                     # iterate through partitions using helper function
        valid_partition=True
        
        for trip in partition:                                                 # check if total wt for trip is below limit 
            cur_wt=0
            
            for cow in trip:
                cur_wt+=cows[cow]           
            if cur_wt>limit:
                valid_partition=False
        
        if valid_partition:                                                    # add algo to list if all trips are acceptable 
            possible_algos.append(partition)                    
            
    min_length=len(cows)
    min_algo=[]
    
    for algo in possible_algos:                                                # find algorith with smallest number of trips 
        if len(algo)<=min_length:
            min_length=len(algo)
            min_algo=algo
        
    return min_algo         

# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    
    cows=load_cows('ps1_cow_data.txt')
    
    start=time.time()                                                  
    algo=greedy_cow_transport(cows)
    min_trips=len(algo)
    end=time.time()
    print('Minimum trips by greddy algorithm:',min_trips)
    print('Time to execute  greedy algorithm:',round(end-start,3))
    
    print()
    
    start=time.time()
    algo=brute_force_cow_transport(cows)
    min_trips=len(algo)
    end=time.time()
    print('Minimum trips by brute force algorithm:',min_trips)
    print('Time to execute  brute force algorithm:',round(end-start,3))
    
"""
Solutions to the Writeup:
    
    1. Greedy algorithm runs much faster. It has to do fewer computations, 
    O(n)=n^2. Brute force must go through a lot more loops, O(n)=2^n.
    
    2. Solution obtained by greedy algorith is sub optimal as it considers only
    a fraction of possible combinations of trips and chooses the best from them.
    
    3. Brute force solution is optimal. It considers all possibilities before 
    making final choice.
    
"""    
    
    
    
    
