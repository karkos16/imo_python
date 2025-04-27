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
        prev_i, next_i = (i - 1), (i + 1) % n
        prev_j, next_j = (j - 1), (j + 1) % n
        old_dist = (distances[route[prev_i], route[i]] + distances[route[prev_j], route[j]] +
                    distances[route[i], route[next_i]] + distances[route[j], route[next_j]])
        new_dist = (distances[route[prev_i], route[j]] + distances[route[j], route[next_i]] +
                    distances[route[prev_j], route[i]] + distances[route[i], route[next_j]])
    return new_dist - old_dist

def compute_shuffle_score_change(route1, route2, distances, i, j):
    a, b = route1[i - 1], route1[i]
    c, d = route1[i + 1], route2[j - 1]
    e, f = route2[j], route2[j + 1]

    old_distance = distances[a, b] + distances[b, c] + distances[d, e] + distances[e, f]
    new_distance = distances[a, e] + distances[e, c] + distances[d, b] + distances[b, f]

    return new_distance - old_distance

def solve_steepest_vertex(starting_routes, distances, _=None):
    """
    Steepest descent optimization: tries best vertex swap or cross-route exchange between two routes.
    """
    route1, route2 = starting_routes
    n = len(route2)
    improved = True

    while improved:
        improved = False
        best_i, best_j = -1, -1
        best_score_change = 0
        use_vertex_method = False  
        best_in_route2 = False    

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                score_change = compute_route_score_change(route1, distances, i, j)
                if score_change < best_score_change:
                    best_score_change = score_change
                    best_i, best_j = i, j
                    use_vertex_method = True
                    best_in_route2 = False

                score_change = compute_route_score_change(route2, distances, i, j)
                if score_change < best_score_change:
                    best_score_change = score_change
                    best_i, best_j = i, j
                    use_vertex_method = True
                    best_in_route2 = True

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                score_change = compute_shuffle_score_change(route1, route2, distances, i, j)
                if score_change < best_score_change:
                    best_score_change = score_change
                    best_i, best_j = i, j
                    use_vertex_method = False

        if best_i != -1 and best_j != -1:
            if use_vertex_method:
                if best_in_route2:
                    route2[best_i], route2[best_j] = route2[best_j], route2[best_i]
                else:
                    route1[best_i], route1[best_j] = route1[best_j], route1[best_i]
            else:
                route1[best_i], route2[best_j] = route2[best_j], route1[best_i]

            improved = True

    return [route1, route2]
