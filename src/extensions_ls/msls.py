from extensions_ls.random_solver import random_solver
from extensions_ls.steepest_moves_list import solve_steepest_moves_list
import sys

sys.path.append('../utils')

from utils.read import calculate_route_length

def solve_msls(distances):
    best_solution = None
    best_length = float('inf')

    for _ in range(200):
        routes = random_solver(distances)
        ls_solution = solve_steepest_moves_list(routes, distances)

        total_length = calculate_route_length(ls_solution[0], distances) + calculate_route_length(ls_solution[1], distances)

        if total_length < best_length:
            best_length = total_length
            best_solution = ls_solution

    return best_solution
