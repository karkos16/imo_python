import time
import matplotlib.pyplot as plt
import utils.read as utils
from construct_alg import greedy_solver, random_solver
from local_search_alg import greedy_local_search_edge_solver, greedy_local_search_vertices_solver, steepest_local_search_edge_solver, steepest_local_search_vertices_solver
from improved_local import steepest_moves_list, steepect_candidate_move
from extensions_ls import msls, ils, lns, lns_without_ls
import os

def plot_route(cities, route1, route2, title):
    x1 = [cities[city_id].coordinates.x for city_id in route1]
    y1 = [cities[city_id].coordinates.y for city_id in route1]
    
    x2 = [cities[city_id].coordinates.x for city_id in route2]
    y2 = [cities[city_id].coordinates.y for city_id in route2]

    plt.figure(figsize=(16, 10), clear=True)
    plt.plot(x1 + [x1[0]], y1 + [y1[0]], 'o-', markersize=4, label="Route 1")
    plt.plot(x2 + [x2[0]], y2 + [y2[0]], 'x-', markersize=4, label="Route 2")

    plt.title(title)
    plt.legend() 

    if not os.path.exists('../plots/new'):
        os.makedirs('../plots/new')

    plt.savefig(f"../plots/new/{title}.png")

if __name__ == "__main__":
    
    instances = [
        "../data/kroA200.tsp",
        "../data/kroB200.tsp",
    ]

    solvers = {
        # "msls": msls.solve_msls,
        # "ils": ils.solve_ils,
        # "lns": lns.solve_lns,
        # "lns_without_ls": lns_without_ls.solve_lns_without_ls,
        # "greedy_local_search_edge": greedy_local_search_edge_solver.solve_greedy_edge,
        # "greedy_local_search_vertices": greedy_local_search_vertices_solver.solve_greedy_vertex,
        # "steepest_local_search_edge": steepest_local_search_edge_solver.solve_steepest_edge,
        "steepest_local_search_vertices": steepest_local_search_vertices_solver.solve_steepest_vertex,
    }
    starters = {
        "greedy_solver": greedy_solver.solve_greedy,
        "random_solver": random_solver.random_solver,
    }

    for instance in instances:
        print(f"\n\nReading instance {instance}...")
        with open(instance, "r") as f:
            content = f.read()
            cities, distances = utils.read_kro_ab_instance(content)
    
        for solver_name, solver in solvers.items():
            for starter_name, starter in starters.items():

                start_routes = starter(distances)
            
                times = []
                lengths = []
                best_route = None
                best_length = float('inf')

                for _ in range(1):
                    start_time = time.perf_counter()
                    route1, route2 = solver(start_routes, distances)
                    end_time = time.perf_counter()
                    
                    total_length = utils.calculate_route_length(route1, distances) + utils.calculate_route_length(route2, distances)
                    run_time = end_time - start_time
                    
                    times.append(run_time)
                    lengths.append(total_length)

                    if total_length < best_length:
                        best_length = total_length
                        best_route = (route1, route2)

                print(f"\nSolver: {solver_name} + {starter_name}")
                print(f"Avg time: {sum(times) / len(times):.4f}s, Min time: {min(times):.4f}s, Max time: {max(times):.4f}s")
                print(f"Avg route length: {sum(lengths) / len(lengths):.2f}, Min length: {min(lengths):.2f}, Max length: {max(lengths):.2f}")

                if best_route:
                    plot_route(cities, best_route[0], best_route[1], title=f"{solver_name} + {starter_name} - {instance.split('/')[-1]}")
