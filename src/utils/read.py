import math
import numpy as np

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        return int(round(math.hypot(self.x - other.x, self.y - other.y)))

class City:
    def __init__(self, id, coordinates):
        self.id = id
        self.coordinates = coordinates

def get_cities(content):
    cities = []
    for line in content.splitlines():
        if line.strip() and all(part.isdigit() for part in line.strip().split()):
            parts = list(map(int, line.strip().split()))
            if len(parts) == 3:
                id, x, y = parts
                cities.append(City(id, Coordinates(x, y)))
    return cities

def read_kro_ab_instance(content):
    cities = get_cities(content)
    n = len(cities)
    distances = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in cities:
        for j in cities:
            distances[i.id - 1][j.id - 1] = i.coordinates.distance_to(j.coordinates)
    
    return cities, np.array(distances)

def calculate_route_length(route, distances):
    return sum(distances[route[i]][route[i+1]] for i in range(len(route)-1))