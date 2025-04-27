import random
import numpy as np

def compute_route_score_change(route, distances, i, j):
    n = len(route)
    if i == 0 or j == 0 or i == n - 1 or j == n - 1:
        return float('inf') 
    elif abs(i - j) == 1:
        b, c = min(i, j), max(i, j)
        a = b - 1
        d = (c + 1) % n
        old_dist = distances[route[a], route[b]] + distances[route[c], route[d]]
        new_dist = distances[route[a], route[c]] + distances[route[b], route[d]]
    else:
        prev_i, next_i = i - 1, (i + 1) % n
        prev_j, next_j = j - 1, (j + 1) % n
        old_dist = (distances[route[prev_i], route[i]] +
                    distances[route[i], route[next_i]] +
                    distances[route[prev_j], route[j]] +
                    distances[route[j], route[next_j]])
        new_dist = (distances[route[prev_i], route[j]] +
                    distances[route[j], route[next_i]] +
                    distances[route[prev_j], route[i]] +
                    distances[route[i], route[next_j]])
    return new_dist - old_dist

def compute_exchange_score_change(route1, route2, distances, i, j):
    a, b = route1[i - 1], route1[i]
    c, d = route1[i + 1], route2[j - 1]
    e, f = route2[j], route2[j + 1]

    old_distance = distances[a, b] + distances[b, c] + distances[d, e] + distances[e, f]
    new_distance = distances[a, e] + distances[e, c] + distances[d, b] + distances[b, f]

    return new_distance - old_distance

def optimize_route(route, distances):
    """
    Local search to optimize a single route (greedy vertex-based swaps).
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
                    route[i], route[j] = route[j], route[i]
                    improved = True
                    break
            if improved:
                break
    return route

def exchange_between_routes(route1, route2, distances):
    """
    Exchange vertices between two routes if it improves the total distance.
    """
    did_exchange = False
    n = len(route2)

    possible_changes = [(i, j) for i in range(1, n - 2) for j in range(i + 1, n - 1)]
    random.shuffle(possible_changes)

    for i, j in possible_changes:
        score_change = compute_exchange_score_change(route1, route2, distances, i, j)
        if score_change < 0:
            route1[i], route2[j] = route2[j], route1[i]
            did_exchange = True

    return route1, route2, did_exchange

def solve_greedy_vertex(starting_routes, distances, _=None):
    """
    Full optimization process: local search + exchanges between two routes.
    """
    route1, route2 = starting_routes
    again = True
    while again:
        route1 = optimize_route(route1, distances)
        route2 = optimize_route(route2, distances)
        route1, route2, again = exchange_between_routes(route1, route2, distances)
    return [route1, route2]
