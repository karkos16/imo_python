import numpy as np

def solve_greedy(distances):
    """
    Solve the TSP 2 cycle problem using a greedy algorithm.
    """
    n = distances.shape[0]
    used = np.zeros(n, dtype=bool)

    start1 = np.random.randint(0, n)
    used[start1] = True
    start2 = np.argmax(distances[start1])

    dists_from_start1 = distances[start1]
    start2 = np.argmax(dists_from_start1 * (~used))  
    used[start2] = True

    route1 = [start1]
    route2 = [start2]

    while len(route1) < n // 2:
        current = route1[-1]
        nearest = find_next(current, used, distances)
        if nearest is not None:
            route1.append(nearest)
            used[nearest] = True

    while len(route2) < n // 2:
        current = route2[-1]
        nearest = find_next(current, used, distances)
        if nearest is not None:
            route2.append(nearest)
            used[nearest] = True

    route1.append(start1)
    route2.append(start2)

    return route1, route2

def find_next(current, used, distances):
    """
    Znajduje najbliższe nieużyte miasto od 'current'
    """
    candidates = np.where(~used)[0]
    if len(candidates) == 0:
        return None
    nearest = candidates[np.argmin(distances[current, candidates])]
    return nearest
