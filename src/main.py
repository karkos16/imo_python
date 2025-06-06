import time
import matplotlib.pyplot as plt
import utils.read as utils
from construct_alg import greedy_solver, random_solver
from genetic import ils, lns, genetic, genetic_without_ls, greedy_cycle, lns_without_ls
from improved_genetic import genetic as improved_genetic
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

    if not os.path.exists('../plots/improved_genetic'):
        os.makedirs('../plots/improved_genetic')

    plt.savefig(f"../plots/improved_genetic/{title}.png")

if __name__ == "__main__":
    
    instances = [
        "../data/kroA200.tsp",
        "../data/kroB200.tsp",
    ]

    solvers = {
        # "msls_solver": msls.solve_msls,
        # "ils_solver": ils.solve_ils,
        # "lns_solver": lns.solve_lns,
        # "lns_without_ls_solver": lns_without_ls.solve_lns_without_ls,
        # "genetic_solver": genetic.solve_genetic,
        # "genetic_without_ls_solver": genetic_without_ls.solve_genetic_without_ls,
        # "greedy_cycle_solver": greedy_cycle.solve_greedy_cycle,
        "improved_genetic_solver": improved_genetic.solve_genetic,
    }

    for instance in instances:
        print(f"\n\nReading instance {instance}...")
        with open(instance, "r") as f:
            content = f.read()
            cities, distances = utils.read_kro_ab_instance(content)
    
        for solver_name, solver in solvers.items():
                times = []
                lengths = []
                iters = []
                best_route = None
                best_length = float('inf')

                for _ in range(5):
                    start_time = time.perf_counter()
                    route1, route2, iterations = solver(distances)
                    end_time = time.perf_counter()
                    
                    total_length = utils.calculate_route_length(route1, distances) + utils.calculate_route_length(route2, distances)
                    run_time = end_time - start_time
                    
                    times.append(run_time)
                    lengths.append(total_length)
                    iters.append(iterations)

                    if total_length < best_length:
                        best_length = total_length
                        best_route = (route1, route2)

                print(f"\nSolver: {solver_name}")
                print(f"Avg time: {sum(times) / len(times):.4f}s, Min time: {min(times):.4f}s, Max time: {max(times):.4f}s")
                print(f"Avg route length: {sum(lengths) / len(lengths):.2f}, Min length: {min(lengths):.2f}, Max length: {max(lengths):.2f}")
                print(f'Avg iters: {sum(iters) / len(iters):.2f}, Min iters: {min(iters):.2f}, Max iters: {max(iters):.2f}')

                if best_route:
                    plot_route(cities, best_route[0], best_route[1], title=f"{solver_name} - {instance.split('/')[-1]}")
