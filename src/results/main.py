from dataclasses import dataclass
from scipy.stats import pearsonr

@dataclass
class Solution:
    length: int
    cycle1: list
    cycle2: list

@dataclass
class SimilarityResult:
    solution_length: int
    edge_similarity: int
    vertex_similarity: int

def read_json(path):
    import json
    with open(path, "r") as f:
        return json.load(f)
    
def cycle_to_edges(cycle: list) -> set:
    edges = set()
    for i in range(len(cycle) - 1):
        u, v = cycle[i], cycle[i + 1]
        edges.add(tuple(sorted((u, v))))
    
    return edges

def edge_similarity(solution1: Solution, solution2: Solution) -> int:
    edges1 = cycle_to_edges(solution1.cycle1) | cycle_to_edges(solution1.cycle2)
    edges2 = cycle_to_edges(solution2.cycle1) | cycle_to_edges(solution2.cycle2)
    return len(edges1 & edges2)

def cycle_similarity_by_vertex(cycle1: list, cycle2: list) -> int:
    set1 = set(cycle1)
    set2 = set(cycle2)
    common_vertices = set1 & set2
    return len(common_vertices)

def vertex_similarity(solution1: Solution, solution2: Solution) -> int:
    sim1 = cycle_similarity_by_vertex(solution1.cycle1, solution2.cycle1) + cycle_similarity_by_vertex(solution1.cycle2, solution2.cycle2)
    sim2 = cycle_similarity_by_vertex(solution1.cycle1, solution2.cycle2) + cycle_similarity_by_vertex(solution1.cycle2, solution2.cycle1)
    return max(sim1, sim2)
    
def plot_similarities(similarities, title, instance_name):
    import matplotlib.pyplot as plt

    x = [sim.solution_length for sim in similarities]
    edge_similarities = [sim.edge_similarity for sim in similarities]
    vertex_similarities = [sim.vertex_similarity for sim in similarities]
    pearson_edge, _ = pearsonr(x, edge_similarities)
    pearson_vertex, _ = pearsonr(x, vertex_similarities)

    plt.figure(figsize=(10, 5))
    plt.scatter(x, edge_similarities, c='blue')
    plt.title(f'Podobieństwo krawędzi - {title} - {instance_name} - Pearson: {pearson_edge:.2f}')
    plt.xlabel("Wartość funkcji celu")
    plt.ylabel("Liczba wspólnych krawędzi")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"plots/{title}_{instance_name}_edge_similarity.png")

    plt.figure(figsize=(10, 5))
    plt.scatter(x, vertex_similarities, c='green')
    plt.title(f'Podobieństwo wierzchołków - {title} - {instance_name} - Pearson: {pearson_vertex:.2f}')
    plt.xlabel("Wartość funkcji celu")
    plt.ylabel("Liczba wspólnych par wierzchołków")
    plt.grid()
    plt.tight_layout()
    plt.savefig(f"plots/{title}_{instance_name}_vertex_similarity.png")

if __name__ == "__main__":
    instances = ["kroA200", "kroB200"]

    for instance in instances:
        greedy_edge_results = read_json(f"{instance}_greedy_edge_results.json")
        genetic_results = read_json(f"{instance}_genetic_results.json")
        greedy_edge_solutions = [Solution(length=result['length'], cycle1=result['cycle1'].split(" "), cycle2=result['cycle2'].split(" ")) for result in greedy_edge_results]
        genetic_solution = Solution(length=genetic_results[0]['length'], cycle1=genetic_results[0]['cycle1'].split(" "), cycle2=genetic_results[0]['cycle2'].split(" "))

        similarities_to_genetic = []
        similarities_to_population = []
        
        for solution in greedy_edge_solutions:
            edge_sim = edge_similarity(solution, genetic_solution)
            vertex_sim = vertex_similarity(solution, genetic_solution)
            similarities_to_genetic.append(SimilarityResult(solution_length=solution.length, edge_similarity=edge_sim, vertex_similarity=vertex_sim))

            tmp_similarities = []
            for other_solution in greedy_edge_solutions:
                if other_solution != solution:
                    edge_sim = edge_similarity(solution, other_solution)
                    vertex_sim = vertex_similarity(solution, other_solution)
                    tmp_similarities.append(SimilarityResult(solution_length=solution.length, edge_similarity=edge_sim, vertex_similarity=vertex_sim))
                    # print(f"Porównanie {solution.length} z {other_solution.length}: krawędzie: {edge_sim}, wierzchołki: {vertex_sim}")

            similarity = SimilarityResult(
                solution_length=solution.length,
                edge_similarity=sum(sim.edge_similarity for sim in tmp_similarities) / len(tmp_similarities),
                vertex_similarity=sum(sim.vertex_similarity for sim in tmp_similarities) / len(tmp_similarities)
            )
            similarities_to_population.append(similarity)

        plot_similarities(similarities_to_genetic, "Zachłanny LS do Genetycznego", instance)
        plot_similarities(similarities_to_population, "Zachłanny LS do reszty populacji", instance)

        



       