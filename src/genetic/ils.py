from extensions_ls.random_solver import random_solver
from extensions_ls.steepest_moves_list import solve_steepest_moves_list
import sys
import numpy as np

sys.path.append('../utils')

from utils.read import calculate_route_length
from time import perf_counter
from copy import deepcopy

def solve_ils(distances):

    def random_swap_2(route1, route2):
        n = len(route1)
        i = np.random.randint(0, n)
        j = np.random.randint(0, n)
        route1[i], route2[j] = route2[j], route1[i]

    def random_swap(route):
        n = len(route)
        i = np.random.randint(0, n)
        j = np.random.randint(0, n)
        route[i], route[j] = route[j], route[i]
        

    def perturbate_solution(routes):
        route1 = deepcopy(routes[0])
        route2 = deepcopy(routes[1])

        for _ in range(5):
            random_swap_2(route1, route2)
        for _ in range(5):
            random_swap(route1)
        for _ in range(5):
            random_swap(route2)

        return [route1, route2]
    
    start_time = perf_counter()
    best_solution = solve_steepest_moves_list(random_solver(distances), distances)
    end_time = perf_counter()
    best_length = calculate_route_length(best_solution[0], distances) + calculate_route_length(best_solution[1], distances)

    times_passed = end_time - start_time
    max_time = 329
    iterations = 0

    while times_passed < max_time:
        start_time = perf_counter()

        perturbated_solution = perturbate_solution(best_solution)

        print(f"Length of route 1: {len(perturbated_solution[0])}")
        print(f"Length of route 2: {len(perturbated_solution[1])}")

        new_solution = solve_steepest_moves_list(perturbated_solution, distances)

        if (len(new_solution[0][:-1]) != len(set(new_solution[0][:-1]))) or (len(new_solution[1][:-1]) != len(set(new_solution[1][:-1]))):
                continue 
        
        new_length = calculate_route_length(new_solution[0], distances) + calculate_route_length(new_solution[1], distances)

        if new_length < best_length:
            best_length = new_length
            best_solution = new_solution
        
        end_time = perf_counter()
        times_passed += end_time - start_time
        iterations += 1

    return best_solution[0], best_solution[1], iterations

    