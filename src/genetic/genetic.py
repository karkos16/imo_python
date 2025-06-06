from genetic.random_solver import random_solver
from genetic.steepest_moves_list import solve_steepest_moves_list
import sys
import numpy as np

sys.path.append('../utils')
from utils.read import calculate_route_length
from time import perf_counter
from copy import deepcopy

def solve_genetic(distances):
    max_time = 329
    iterations = 0
    population_size = 20
    
    population = {}

    best_solution = None
    best_length = float('inf')

    def initialize_population():
        while len(population) < population_size:
            routes = random_solver(distances)
            ls_solution = solve_steepest_moves_list(routes, distances)

            if (len(ls_solution[0][:-1]) != len(set(ls_solution[0][:-1]))) or (len(ls_solution[1][:-1]) != len(set(ls_solution[1][:-1]))):
                continue

            total_length = calculate_route_length(ls_solution[0], distances) + calculate_route_length(ls_solution[1], distances)

            if population.get(total_length) is None:
                population[total_length] = ls_solution

    def to_edges(cycle):
        n = len(cycle)
        return [(cycle[i], cycle[(i + 1) % n]) for i in range(n)]

    def shift_to_same_start(cycle, start):
        cycle = cycle[cycle.index(start):] + cycle[:cycle.index(start)]
        return cycle
    
    def get_difference_indexes(cycle1, cycle2):
        n = len(cycle1)

        common = set(cycle1) & set(cycle2)
        if len(common) == 0:
            return None
        
        common_vertex = next(iter(common))

        shifted_cycle1 = shift_to_same_start(cycle1, common_vertex)
        shifted_cycle2 = shift_to_same_start(cycle2, common_vertex)

        edges1 = to_edges(shifted_cycle1)
        edges2 = to_edges(shifted_cycle2)

        visited = [False] * n
        max_len = 0
        best_start = None

        for i in range(n):
            if visited[i] or edges1[i] == edges2[i]:
                continue

            # rozpoczęcie nowej niespójności
            start = i
            length = 0
            j = i

            while not visited[j] and edges1[j] != edges2[j]:
                visited[j] = True
                length += 1
                j = (j + 1) % n

            if length > max_len:
                max_len = length
                best_start = start

        
        return best_start
    

    def remove_edges(cycle, start, percentage=0.3):
        n = len(cycle)
        length_to_remove = int(n * percentage)
        end_index = (start + length_to_remove) % n

        removed = []
        new_cycle = []

        if start <= end_index:
            removed = cycle[start:end_index + 1]
            new_cycle = cycle[end_index + 1:] + cycle[:start]
        else:
            removed = cycle[start:] + cycle[:end_index + 1]
            new_cycle = cycle[end_index + 1:start]

        return (new_cycle, removed)
        
    def repair_solution(routes, removed_cities):
        route1 = list(deepcopy(routes[0]))
        route2 = list(deepcopy(routes[1]))

        if len(removed_cities) != len(set(removed_cities)):
            print("Error: removed_cities has duplicates")
            exit()

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
        
        return [route1, route2]

    def recombine(soulution1, solution2):
        first_cycle1 = deepcopy(soulution1[0][:-1])
        first_cycle2 = deepcopy(solution2[0][:-1])
        second_cycle1 = deepcopy(soulution1[1][:-1])
        second_cycle2 = deepcopy(solution2[1][:-1])

        start1 = get_difference_indexes(first_cycle1, first_cycle2)
        start2 = get_difference_indexes(second_cycle1, second_cycle2)

        new_cycle1, removed1 = (remove_edges(first_cycle1, start1)) if start1 is not None else (first_cycle1, [])
        new_cycle2, removed2 = (remove_edges(second_cycle1, start2)) if start2 is not None else (second_cycle1, [])
        
        removed_cities = set(removed1 + removed2)

        new_cycle1, new_cycle2 = repair_solution([new_cycle1, new_cycle2], removed_cities)

        return (new_cycle1, new_cycle2)


    time_passed = perf_counter()
    initialize_population()
    best_length = min(population.keys())
    best_solution = population[best_length]
    time_passed = perf_counter() - time_passed

    while time_passed < max_time:
        start_time = perf_counter()

        solution1 = np.random.choice(list(population.keys()))

        while True:
            solution2 = np.random.choice(list(population.keys()))
            if solution1 != solution2:
                break

        solution1 = population[solution1]
        solution2 = population[solution2]

        new_solution = recombine(solution1, solution2)

        if (len(new_solution[0][:-1]) != len(set(new_solution[0][:-1]))) or (len(new_solution[1][:-1]) != len(set(new_solution[1][:-1]))):
            continue
        if len(new_solution[0])  != 101 or len(new_solution[1]) != 101:
            continue

        new_solution = solve_steepest_moves_list(new_solution, distances)
        if (len(new_solution[0][:-1]) != len(set(new_solution[0][:-1]))) or (len(new_solution[1][:-1]) != len(set(new_solution[1][:-1]))):
            continue

        new_length = calculate_route_length(new_solution[0], distances) + calculate_route_length(new_solution[1], distances)
        
        if new_length < max(population.keys()) and new_length not in population:
            population[new_length] = new_solution
            del population[max(population.keys())]

        if new_length < best_length:
            best_length = new_length
            best_solution = new_solution

        time_passed += perf_counter() - start_time
        iterations += 1
    
    return best_solution[0], best_solution[1], iterations
