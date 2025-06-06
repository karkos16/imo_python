from local_search_alg import greedy_local_search_edge_solver
from construct_alg import random_solver
from genetic import genetic
import utils.read as utils
import json

if __name__ == "__main__":
    instances = [
        "../data/kroA200.tsp",
        "../data/kroB200.tsp",
    ]

    for instance in instances:
        results = []
        with open(instance, "r") as f:
            content = f.read()
            cities, distances = utils.read_kro_ab_instance(content)
        
        for _ in range(1000):
            starting_routes = random_solver.random_solver(distances)
            best_routes = greedy_local_search_edge_solver.solve_greedy_edge(starting_routes, distances)

            length = utils.calculate_route_length(best_routes[0], distances) + utils.calculate_route_length(best_routes[1], distances)
            cycle1 = best_routes[0]
            cycle2 = best_routes[1]
            results.append({
                "length": int(length),
                "cycle1": " ".join(str(x) for x in cycle1),
                "cycle2": " ".join(str(x) for x in cycle2),
            })

        instance_name = instance.split("/")[-1].split(".")[0]
        with open(f"results/{instance_name}_greedy_edge_results.json", "w") as f:
            json.dump(results, f, indent=2)
        