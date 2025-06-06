from utils.read import calculate_route_length
from collections import deque

def solve_steepest_moves_list(initial_routes, distances):
    route1 = initial_routes[0]
    route2 = initial_routes[1]
    n = len(route2)

    def edge_in_edges(edge, edge_list):
        return edge in edge_list or (edge[1], edge[0]) in edge_list
    
    def is_move_applicable(removed_edges, route1, route2):
        current_edges = {(route1[i], route1[(i + 1) % n]) for i in range(n)}
        current_edges.update((route2[i], route2[(i + 1) % n]) for i in range(n))
        
        same_direction = True
        for e in removed_edges:
            if e not in current_edges and (e[1], e[0]) not in current_edges:
                return "remove" 
            elif e not in current_edges:
                same_direction = False
        return "apply" if same_direction else "skip"

    def add_new_moves(LM, route1, route2, distances, recent_move):
        tmoves = []
        
        if recent_move is None:
            for i in range(n):
                for j in range(n):
                    tmoves.append((i, j, "swap"))
            for route, route_id in [(route1, 1), (route2, 2)]:
                for i in range(len(route)):
                    for j in range(i + 1, len(route)):
                        tmoves.append((i, j, "edge_swap", route_id))
        
        else:
            if recent_move[0] == "swap":
                i, j = recent_move[1], recent_move[2]
                
                indices1 = {i, (i - 1) % n, (i + 1) % n}
                indices2 = {j, (j - 1) % n, (j + 1) % n}
                
                for ni in indices1:
                    for nj in range(n):
                        tmoves.append((ni, nj, "swap"))
                for nj in indices2:
                    for ni in range(n):
                        tmoves.append((ni, nj, "swap"))
                
                for idx in indices1:
                    for jdx in range(n):
                        if idx != jdx:
                            tmoves.append((min(idx, jdx), max(idx, jdx), "edge_swap", 1))
                for idx in indices2:
                    for jdx in range(n):
                        if idx != jdx:
                            tmoves.append((min(idx, jdx), max(idx, jdx), "edge_swap", 2))
            elif recent_move[0] == "edge_swap":
                i, j, route_id = recent_move[1], recent_move[2], recent_move[3]
                current_route = route1 if route_id == 1 else route2
                
                affected_indices = [k % len(current_route) for k in range(i - 1, j + 2)]
                
                for a in affected_indices:
                    for b in range(a + 1, a + len(current_route)):
                        idx_b = b % len(current_route)
                        tmoves.append((min(a, idx_b), max(a, idx_b), "edge_swap", route_id))
                affected_nodes = {current_route[k] for k in affected_indices}
                
                for i, v1 in enumerate(route1):
                    if v1 in affected_nodes:
                        for j in range(n):
                            tmoves.append((i, j, "swap"))
                for j, v2 in enumerate(route2):
                    if v2 in affected_nodes:
                        for i in range(n):
                            tmoves.append((i, j, "swap"))
        
        for move in tmoves:
            if move[2] == "swap":
                i, j = move[0], move[1]
                try:
                    a, b = route1[i], route2[j]
                    prev_i, next_i = route1[(i - 1) % n], route1[(i + 1) % n]
                    prev_j, next_j = route2[(j - 1) % n], route2[(j + 1) % n]
                except IndexError:
                    continue
                delta = -distances[prev_i][a] - distances[a][next_i]
                delta -= distances[prev_j][b] + distances[b][next_j]
                delta += distances[prev_i][b] + distances[b][next_i]
                delta += distances[prev_j][a] + distances[a][next_j]
                if delta < 0:
                    LM.append([("swap", i, j), delta, [(prev_i, a), (a, next_i), (prev_j, b), (b, next_j)]])
            else:
                i, j, _, route_id = move
                if i == j:
                    continue
                current_route = route1 if route_id == 1 else route2
                a, b = current_route[i], current_route[(i + 1) % len(current_route)]
                c, d = current_route[j], current_route[(j + 1) % len(current_route)]
                delta = -distances[a][b] - distances[c][d]
                delta += distances[a][c] + distances[b][d]
                if delta < 0:
                    LM.append([("edge_swap", i, j, route_id), delta, [(a, b), (c, d)]])

    def update_LM_after_move(LM, last_move, route1, route2, distances):
        def is_affected(move_data, changed_nodes, removed_edges):
            if move_data[0] == "swap":
                _, i, j = move_data
                try:
                    v1, v2 = route1[i], route2[j]
                    return v1 in changed_nodes or v2 in changed_nodes
                except IndexError:
                    return True
            elif move_data[0] == "edge_swap":
                _, i, j, route_id = move_data
                current_route = route1 if route_id == 1 else route2
                e1 = (current_route[i], current_route[(i + 1) % len(current_route)])
                e2 = (current_route[j], current_route[(j + 1) % len(current_route)])
                return edge_in_edges(e1, removed_edges) or edge_in_edges(e2, removed_edges)
            return False

        if last_move[0] == "swap":
            i, j = last_move[1], last_move[2]
            changed_nodes = {
                route1[i], route2[j],
                route1[(i - 1) % n], route1[(i + 1) % n],
                route2[(j - 1) % n], route2[(j + 1) % n]
            }
            removed_edges = [
                (route1[(i - 1) % n], route1[i]),
                (route1[i], route1[(i + 1) % n]),
                (route2[(j - 1) % n], route2[j]),
                (route2[j], route2[(j + 1) % n])
            ]
        else:
            i, j, route_id = last_move[1], last_move[2], last_move[3]
            current_route = route1 if route_id == 1 else route2
            start, end = (i - 1) % len(current_route), (j + 1) % len(current_route)
            if start <= end:
                changed_nodes = set(current_route[k] for k in range(start, end + 1))
                removed_edges = [(current_route[k], current_route[(k + 1) % len(current_route)]) for k in range(start, end)]
            else:
                indices = list(range(start, len(current_route))) + list(range(0, end + 1))
                changed_nodes = set(current_route[k] for k in indices)
                removed_edges = [(current_route[k], current_route[(k + 1) % len(current_route)]) for k in indices[:-1]]

        LM = [move for move in LM if not is_affected(move[0], changed_nodes, removed_edges)]
        add_new_moves(LM, route1, route2, distances, last_move)
        return sorted(LM, key=lambda x: (x[1], x[0][1], x[0][2], -ord(x[0][0][0])))


    current_cost = calculate_route_length(route1, distances) + calculate_route_length(route2, distances)
    LM = deque()
    add_new_moves(LM, route1, route2, distances, None)
    LM = deque(sorted(LM, key=lambda x: (x[1], x[0][1], x[0][2], -ord(x[0][0][0]))))

    while True:
        best_move = None
        length = len(LM)
        for _ in range(length):
            move = LM.popleft()
            move_data, delta, removed_edges = move
            applicability = is_move_applicable(removed_edges, route1, route2)

            if applicability == "remove":
                continue 
            elif applicability == "skip":
                LM.append(move)  
            elif applicability == "apply":
                best_move = move
                break

        if not best_move:
            break  

        
        move_data, delta, removed_edges = best_move
        if move_data[0] == "swap":
            i, j = move_data[1], move_data[2]
            route1[i], route2[j] = route2[j], route1[i]
        else:
            i, j, route_id = move_data[1], move_data[2], move_data[3]
            current_route = route1 if route_id == 1 else route2
            segment = [current_route[(k) % len(current_route)] for k in range(i + 1, j + 1)]
            for k, idx in enumerate(range(i + 1, j + 1)):
                current_route[idx % len(current_route)] = segment[-(k + 1)]
        
        current_cost += delta
        
        LM = deque(update_LM_after_move(list(LM), move_data, route1, route2, distances))
        
    return [route1, route2]
