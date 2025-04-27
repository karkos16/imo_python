import random
import numpy as np

def compute_route_score_change(route, distances, i, j):
    prev_i = i - 1
    prev_j = j - 1

    old_dist = distances[route[prev_i], route[i]] + distances[route[prev_j], route[j]]
    new_dist = distances[route[prev_i], route[prev_j]] + distances[route[i], route[j]]

    return new_dist - old_dist

def compute_exchange_score_change(route1, route2, distances, i, j):
    a, b = route1[i - 1], route1[i]
    c, d = route1[i + 1], route2[j - 1]
    e, f = route2[j], route2[j + 1]

    old_dist = distances[a, b] + distances[b, c] + distances[d, e] + distances[e, f]
    new_dist = distances[a, e] + distances[e, c] + distances[d, b] + distances[b, f]

    return new_dist - old_dist

def optimize_route(route, distances):
    """
    Local search 2-opt on a single route.
    """
    n = len(route)
    improved = True
    while improved:
        improved = False
        indices = list(range(1, n - 1))
        random.shuffle(indices)
        for i in indices:
            for j in range(i + 1, n):
                score_change = compute_route_score_change(route, distances, i, j)
                if score_change < 0:
                    if abs(i - j) == 1:
                        route[i], route[j] = route[j], route[i]
                    else:
                        route[i:j] = route[i:j][::-1]
                    improved = True
                    break
            if improved:
                break
    return route

def exchange_between_routes(route1, route2, distances):
    """
    Try exchanging vertices between two routes to improve the solution.
    """
    did_exchange = False
    n = len(route2)

    possible_changes = []
    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            possible_changes.append((i, j))
    random.shuffle(possible_changes)

    for i, j in possible_changes:
        score_change = compute_exchange_score_change(route1, route2, distances, i, j)
        if score_change < 0:
            route1[i], route2[j] = route2[j], route1[i]
            did_exchange = True

    return route1, route2, did_exchange

def solve_greedy_edge(starting_routes, distances, _=None):
    """
    Main local optimization: 2-opt on both routes and exchanges between them.
    """
    route1, route2 = starting_routes
    improved = True
    while improved:
        route1 = optimize_route(route1, distances)
        route2 = optimize_route(route2, distances)
        route1, route2, improved = exchange_between_routes(route1, route2, distances)
    return [route1, route2]
