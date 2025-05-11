import numpy as np

def random_solver(distances):
    """
    Solve the TSP 2 cycle problem using random choices.
    """
    n = distances.shape[0]
    used = np.zeros(n, dtype=bool)

    start1 = np.random.randint(0, n)
    used[start1] = True

    dists_from_start1 = distances[start1]
    start2 = np.argmax(dists_from_start1 * (~used))
    used[start2] = True

    route1 = [start1]
    route2 = [start2]

    while len(route1) < n // 2:
        next_city = find_random_next(used)
        if next_city is not None:
            route1.append(next_city)
            used[next_city] = True

    while len(route2) < n // 2:
        current = route2[-1]
        next_city = find_random_next(used)
        if next_city is not None:
            route2.append(next_city)
            used[next_city] = True

    route1.append(start1)
    route2.append(start2)

    return route1, route2

def find_random_next(used):
    """
    Losowo wybiera nieużyte miasto.
    """
    candidates = np.where(~used)[0]
    if len(candidates) == 0:
        return None
    return np.random.choice(candidates)
