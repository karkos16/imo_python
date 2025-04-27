import numpy as np
from utils.read import calculate_route_length

def solve_candidate_swaps(initial_routes, distances):
    route1 = initial_routes[0]
    route2 = initial_routes[1]
    n = len(route2)
    
    def generate_candidate_edges(distances, k=10):
        num_nodes = len(distances)
        candidate_edges = {}
        for i in range(num_nodes):
            neighbors = np.argsort(distances[i])[1:k+1]
            candidate_edges[i] = set(neighbors)
        return candidate_edges

    candidate_edges = generate_candidate_edges(distances)
    
    improvement_found = True
    current_cost = calculate_route_length(route1, distances) + calculate_route_length(route2, distances)

    while improvement_found:
        improvement_found = False
        best_delta = 0
        best_move = None

        for i in range(n):
            for j in range(n):
                a, b = route1[i], route2[j]

                if b not in candidate_edges[a] and a not in candidate_edges[b]:
                    continue
                
                a_prev = route1[i - 1]
                a_next = route1[(i + 1) % n]
                b_prev = route2[j - 1]
                b_next = route2[(j + 1) % n]

                delta = 0
                delta -= distances[a_prev][a] + distances[a][a_next]
                delta -= distances[b_prev][b] + distances[b][b_next]
                delta += distances[a_prev][b] + distances[b][a_next]
                delta += distances[b_prev][a] + distances[a][b_next]

                if delta < best_delta:
                    best_delta = delta
                    best_move = ("swap", i, j)

        for route in [route1, route2]:
            n = len(route)
            for i in range(n):
                n1 = route[i]
                next_i = (i + 1) % n
                prev_i = (i - 1) % n
                for j in range(n):
                    if i == j:
                        continue
                    n2 = route[j]
                    if n2 not in candidate_edges[n1]:
                        continue

                    next_j = (j + 1) % n
                    prev_j = (j - 1) % n

                    a, b = n1, route[next_i]
                    c, d = n2, route[next_j]
                    if len({a, b, c, d}) == 4:
                        delta = -distances[a][b] - distances[c][d] + distances[a][c] + distances[b][d]
                        if (c in candidate_edges[a] or a in candidate_edges[c]):
                            if delta < best_delta:
                                best_delta = delta
                                best_move = ("intra_next", i, j, route)

                    a, b = route[prev_i], n1
                    c, d = route[prev_j], n2
                    if len({a, b, c, d}) == 4:
                        delta = -distances[a][b] - distances[c][d] + distances[a][c] + distances[b][d]
                        if b in candidate_edges[d] or d in candidate_edges[b]:
                            if delta < best_delta:
                                best_delta = delta
                                best_move = ("intra_prev", i, j, route)

        if best_move:
            improvement_found = True
            move_type = best_move[0]

            if move_type == "swap":
                i, j = best_move[1], best_move[2]
                route1[i], route2[j] = route2[j], route1[i]

            elif move_type == "intra_next":
                i, j, route = best_move[1:]
                i_next = (i + 1) % len(route)
                j_next = (j + 1) % len(route)
                if i_next < j:
                    route[i_next:j + 1] = reversed(route[i_next:j + 1])
                else:
                    route[j_next:i + 1] = reversed(route[j_next:i + 1])

            elif move_type == "intra_prev":
                i, j, route = best_move[1:]
                i_prev = (i - 1) % len(route)
                j_prev = (j - 1) % len(route)
                if j < i_prev:
                    route[j:i_prev + 1] = reversed(route[j:i_prev + 1])
                else:
                    route[i:j_prev + 1] = reversed(route[i:j_prev + 1])

            current_cost += best_delta

    return [route1, route2]
