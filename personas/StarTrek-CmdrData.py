"""
"""

input = """a 1 b 2
a 1 c 4
b 2 c 4
b 2 d 0
b 3 b 2
b 3 e 2
c 4 d 0
c 4 e 1"""

import sys
from collections import defaultdict, deque

def read_input():
    dependencies = []
    for line in input.strip().split("\n"):
        parts = line.strip().split()
        if len(parts) == 4:
            dependencies.append((parts[0], int(parts[1]), parts[2], int(parts[3])))
    return dependencies

def build_graph(dependencies):
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    for depender, depender_ver, dependee, dependee_ver in dependencies:
        reverse_graph[(dependee, dependee_ver)].append((depender, depender_ver))
    return graph, reverse_graph

def calculate_dependents(graph):
    direct_count = defaultdict(int)
    transitive_sets = defaultdict(set)

    # First collect direct dependants
    for node, dependants in graph.items():
        for dependant in dependants:
            direct_count[node] += 1
            transitive_sets[dependant].add(node)

    # Calculate transitive dependants using DFS to avoid modification during traversal
    def dfs(node, visited):
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                transitive_sets[neighbour].update(transitive_sets[node])
                dfs(neighbour, visited)

    nodes = list(graph.keys())  # List of all nodes to avoid dict size change error
    for node in nodes:
        dfs(node, set([node]))

    transitive_count = {node: len(dependents) for node, dependents in transitive_sets.items()}
    return transitive_count, direct_count

def find_most_problematic(transitive_count, direct_count):
    max_ratio = -1
    problematic_package = None
    for node in direct_count:
        if direct_count[node] > 0:  # Ensure we have direct dependants to avoid division by zero
            trans = transitive_count.get(node, 0)
            ratio = trans / direct_count[node]
            if ratio > max_ratio:
                max_ratio = ratio
                problematic_package = node
    return problematic_package

def main():
    dependencies = read_input()
    _, reverse_graph = build_graph(dependencies)
    transitive_count, direct_count = calculate_dependents(reverse_graph)
    problematic_package = find_most_problematic(transitive_count, direct_count)
    if problematic_package:
        print(f"{problematic_package[0]} {problematic_package[1]}")
    else:
        print("No problematic dependencies found.")

if __name__ == "__main__":
    main()
