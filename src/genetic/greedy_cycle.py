import sys
import numpy as np

sys.path.append('../utils')

from utils.read import calculate_route_length

def solve_greedy_cycle(distances):
    start1 = np.random.randint(0, len(distances))
    start2 = np.argmax([distances[start1][j] for j in range(len(distances)) if j != start1])

    route1 = [start1]
    route2 = [start2]
    visited = {start1, start2}

    while len(visited) < len(distances):
        nearest1 = np.argmin([calculate_route_length(route1 + [j, start1], distances) if j not in visited else float('inf') for j in range(len(distances))])
        nearest2 = np.argmin([calculate_route_length(route2 + [j, start2], distances) if j not in visited else float('inf') for j in range(len(distances))])
        if nearest1 == nearest2:
            if len(route1) < 100:
                route1.append(nearest1)
                visited.add(nearest1)
            elif len(route2) < 100:
                route2.append(nearest2)
                visited.add(nearest2)
            continue

        if len(route1) < 100:
            route1.append(nearest1)
            visited.add(nearest1)
        
        if len(route2) < 100:
            route2.append(nearest2)
            visited.add(nearest2)


    route1.append(start1)
    route2.append(start2)

    return route1, route2, 0