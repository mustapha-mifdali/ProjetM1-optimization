import random

# ==========================================
# 1. INITIALIZATION & EVALUATION
# ==========================================

def create_initial_tour(num_cities):
    """
    Creates a random initial route (a permutation of cities).
    Example for 5 cities: [2, 0, 4, 1, 3]
    """
    tour = list(range(num_cities))
    random.shuffle(tour)
    return tour

def calculate_route_distance(route, distance_matrix):
    """
    Calculates the total distance of a given route using the distance matrix.
    Includes the return trip from the last city back to the first.
    """
    total_distance = 0
    num_cities = len(route)
    
    for i in range(num_cities):
        current_city = route[i]
        next_city = route[(i + 1) % num_cities] # Wraps around to 0 at the end
        total_distance += distance_matrix[current_city][next_city]
        
    return total_distance


# ==========================================
# 2. SWAP NEIGHBORHOOD (For basic algorithms)
# ==========================================
# 

def generate_random_swap_neighbor(tour):
    """
    Picks two random positions and swaps the cities at those positions.
    (Used mainly for Simulated Annealing)
    """
    new_tour = tour.copy() 
    n = len(tour)
    
    # Choose two different random indices
    i, j = random.sample(range(n), 2)
    
    # Swap the cities
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    
    return new_tour

def generate_all_swap_neighbors(tour):
    """
    Generates a list of ALL possible neighbors by swapping 2 by 2.
    (Used mainly for Hill-Climbing Best/First Improvement)
    """
    neighbors = []
    n = len(tour)
    
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = tour.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
            
    return neighbors


# ==========================================
# 3. 2-OPT NEIGHBORHOOD (Optional but highly recommended)
# ==========================================
# 

def generate_2opt_neighbor(tour, i, j):
    """
    Reverses the order of the cities in the segment from index i to index j.
    Assumes i < j.
    """
    # Keep the start, reverse the middle part, keep the end
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour

def generate_random_2opt_neighbor(tour):
    """
    Generates a single random 2-opt neighbor.
    (Can be used as an upgrade for Simulated Annealing)
    """
    n = len(tour)
    # Pick two random indices and make sure i < j using sorted()
    i, j = sorted(random.sample(range(n), 2))
    
    return generate_2opt_neighbor(tour, i, j)

def generate_all_2opt_neighbors(tour):
    """
    Generates a list of ALL possible 2-opt neighbors.
    (Can be used as an upgrade for Hill-Climbing)
    """
    neighbors = []
    n = len(tour)
    for i in range(n - 1):
        for j in range(i + 1, n):
            neighbors.append(generate_2opt_neighbor(tour, i, j))
    return neighbors