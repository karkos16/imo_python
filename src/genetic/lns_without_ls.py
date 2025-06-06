from extensions_ls.random_solver import random_solver
from extensions_ls.steepest_moves_list import solve_steepest_moves_list
import sys
import numpy as np

sys.path.append('../utils')

from utils.read import calculate_route_length
from time import perf_counter
from copy import deepcopy

def solve_lns_without_ls(distances):

    def find_closest_between_cycles(route1, route2):
        min_distance = float('inf')
        best_pair = None

        for i in range(len(route1)):
            for j in range(len(route2)):
                distance = distances[route1[i]][route2[j]]
                if distance < min_distance:
                    min_distance = distance
                    best_pair = ((route1[i], i), (route2[j], j))

        return best_pair

    def destroy_solution(routes):
        route1 = deepcopy(routes[0][:-1])
        route2 = deepcopy(routes[1][:-1])

        removed_cities = []

        closest_pair = find_closest_between_cycles(route1, route2)

        (_, idx1), (_, idx2) = closest_pair

        if np.random.random() < 0.2:
            idx1 = np.random.randint(0, len(route1))
            idx2 = np.random.randint(0, len(route2))

        def get_indices_to_remove(route_length, center_idx, window=14):
            return set([(center_idx + i) % route_length for i in range(-window, window + 1)])

        indices_to_remove1 = get_indices_to_remove(len(route1), idx1)
        indices_to_remove2 = get_indices_to_remove(len(route2), idx2)

        for i in indices_to_remove1:
            removed_cities.append(route1[i])
            route1[i] = -1
        for i in indices_to_remove2:
            removed_cities.append(route2[i])
            route2[i] = -1

        need_change_order1 = route1[0] != -1 and route1[-1] != -1
        need_change_order2 = route2[0] != -1 and route2[-1] != -1

        first_minus1 = route1.index(-1)
        last_minus1 = len(route1) - 1 - route1[::-1].index(-1)
        first_minus2 = route2.index(-1)
        last_minus2 = len(route2) - 1 - route2[::-1].index(-1)

        new_route1 = route1[last_minus1 + 1:] + route1[:first_minus1] if need_change_order1 else [city for city in route1 if city != -1]
        new_route2 = route2[last_minus2 + 1:] + route2[:first_minus2] if need_change_order2 else [city for city in route2 if city != -1]

        if len(removed_cities) != len(set(removed_cities)):
            return None, None

        return list(removed_cities), [new_route1, new_route2]
    
    def repair_solution(routes, removed_cities):
        route1 = deepcopy(routes[0])
        route2 = deepcopy(routes[1])

        while removed_cities:
            best_city1 = None
            best_city2 = None
            distance1 = float('inf')
            distance2 = float('inf')

            for removed_city in removed_cities:
                distance_tmp1= distances[route1[-1]][removed_city] + distances[removed_city][route1[0]] if distances[route1[-1]][removed_city] + distances[removed_city][route1[0]] < distance1 else float('inf')
                distance_tmp2 = distances[route2[-1]][removed_city] + distances[removed_city][route2[0]] if distances[route2[-1]][removed_city] + distances[removed_city][route2[0]] < distance2 else float('inf')

                if distance_tmp1 < distance1:
                    distance1 = distance_tmp1
                    best_city1 = removed_city
                if distance_tmp2 < distance2:
                    distance2 = distance_tmp2
                    best_city2 = removed_city

            if best_city1 == best_city2 and len(route1) < 100 and len(route2) < 100:
                if distance1 <= distance2 and len(route1) < 100:
                    route1.append(best_city1)
                    removed_cities.remove(best_city1)
                elif len(route2) < 100:
                    route2.append(best_city2)
                    removed_cities.remove(best_city2)
            else:
                if (len(route1) < 100):
                    route1.append(best_city1)
                    removed_cities.remove(best_city1)
                if (len(route2) < 100):
                    route2.append(best_city2)
                    removed_cities.remove(best_city2)

        route1.append(route1[0])
        route2.append(route2[0])

        if len(route1[:-1]) != len(set(route1[:-1])):
            return []
        
        if len(route2[:-1]) != len(set(route2[:-1])):
            return []
        return route1, route2

    

    start_time = perf_counter()
    best_solution = solve_steepest_moves_list(random_solver(distances), distances)
    end_time = perf_counter()

    best_length = calculate_route_length(best_solution[0], distances) + calculate_route_length(best_solution[1], distances)

    times_passed = end_time - start_time
    max_time = 329
    iterations = 0

    while (len(best_solution[0][:-1]) != len(set(best_solution[0][:-1]))) or (len(best_solution[1][:-1]) != len(set(best_solution[1][:-1]))):
        best_solution = solve_steepest_moves_list(random_solver(distances), distances)

    while times_passed < max_time:
        start_time = perf_counter()
        removed_cities, new_solution = destroy_solution(best_solution)

        if removed_cities is None or new_solution is None:
            continue

        new_solution = repair_solution(new_solution, removed_cities)

        if new_solution == []:
            continue

        if (len(new_solution[0][:-1]) != len(set(new_solution[0][:-1]))) or (len(new_solution[1][:-1]) != len(set(new_solution[1][:-1]))):
            continue
        if len(new_solution[0]) != 101 or len(new_solution[1]) != 101:
            continue

        new_length = calculate_route_length(new_solution[0], distances) + calculate_route_length(new_solution[1], distances)

        if new_length < best_length:
            best_length = new_length
            best_solution = new_solution

        end_time = perf_counter()
        times_passed += end_time - start_time
        iterations += 1

    return best_solution[0], best_solution[1], iterations
